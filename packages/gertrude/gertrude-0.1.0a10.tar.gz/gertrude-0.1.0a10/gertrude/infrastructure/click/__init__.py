# Gertrude --- GTD done right
# Copyright © 2020-2023 Tanguy Le Carrour <tanguy@bioneland.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging

import click
from bles import Projectionist
from blessql.projections import REGISTRY, Ledger
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from gertrude.application import projectors
from gertrude.infrastructure.requests import HttpEventStore
from gertrude.infrastructure.settings import CliSettings
from gertrude.infrastructure.sqlalchemy import projections, repositories

level = logging.DEBUG
str_fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S %z"
logging.basicConfig(format=str_fmt, level=level, datefmt=date_fmt)


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass


@cli.group()
@click.pass_context
def db(ctx: click.Context) -> None:
    pass


@db.command()
@click.pass_context
def initialise(ctx: click.Context) -> None:
    """Initialise DB."""

    click.echo("Initialising DB schemas…")
    create_tables("ledger", ctx.obj.PROJECTION_DSN, REGISTRY.metadata)
    create_tables("projections", ctx.obj.PROJECTION_DSN, projections.METADATA)
    create_tables("data", ctx.obj.DATA_DSN, repositories.REGISTRY.metadata)


def create_tables(schema: str, dsn: str, metadata: MetaData) -> None:
    click.echo(f"Initialising schema `{schema}`.")
    engine = create_engine(dsn)
    metadata.create_all(engine)


def build_projectionist(url: str, session: Session) -> Projectionist:
    projectionist = Projectionist(HttpEventStore(url), Ledger(session))
    projectionist.register(projectors.Tasks(projections.Tasks(session)))
    return projectionist


@cli.group()
@click.pass_context
def projectionist(ctx: click.Context) -> None:
    pass


@projectionist.command()
@click.pass_context
def boot(ctx: click.Context) -> None:
    """Boot the projections."""

    create_tables("projections", ctx.obj.PROJECTION_DSN, projections.METADATA)

    click.echo("Booting projections…")
    with sessionmaker(bind=create_engine(ctx.obj.PROJECTION_DSN))() as session:
        projectionist = build_projectionist(ctx.obj.EVENT_STORE_URL, session)
        projectionist.boot()
        session.commit()


@projectionist.command()
@click.pass_context
def start(ctx: click.Context) -> None:
    """Start the projection manager."""

    click.echo("Starting projections…")
    with sessionmaker(bind=create_engine(ctx.obj.PROJECTION_DSN))() as session:
        projectionist = build_projectionist(ctx.obj.EVENT_STORE_URL, session)
        projectionist.play(follow=True)
        session.commit()


def build(settings: CliSettings) -> click.Group:
    return cli(obj=settings)  # type: ignore[no-any-return]
