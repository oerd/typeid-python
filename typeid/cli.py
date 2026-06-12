import click
from uuid_utils.compat import UUID

from typeid import TypeID
from typeid import base32
from typeid import from_uuid
from typeid import get_prefix_and_suffix


@click.group()
def cli():
    pass


@cli.command()
@click.option("-p", "--prefix")
def new(prefix: str | None = None) -> None:
    typeid = TypeID(prefix=prefix)
    click.echo(str(typeid))


@cli.command()
@click.argument("uuid")
@click.option("-p", "--prefix")
def encode(uuid: str, prefix: str | None = None) -> None:
    typeid = from_uuid(suffix=UUID(uuid), prefix=prefix)
    click.echo(str(typeid))


@cli.command()
@click.argument("encoded")
def decode(encoded: str) -> None:
    prefix, suffix = get_prefix_and_suffix(encoded)

    uuid = UUID(bytes=base32.decode(suffix))

    click.echo(f"type: {prefix}")
    click.echo(f"uuid: {uuid}")


if __name__ == "__main__":
    cli()
