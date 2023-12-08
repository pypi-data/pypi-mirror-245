from pathlib import Path
from typing import Optional

from sparv.api import Config, Corpus, MarkerOptional, OutputMarker, Source, installer, uninstaller, util


@installer("Passthrough installer", uninstaller="passthrough:uninstall")
def install(
    corpus: Corpus = Corpus(),
    source_dir: Source = Source(),
    marker: OutputMarker = OutputMarker("passthrough.install_marker"),
    uninstall_marker: MarkerOptional = MarkerOptional("passthrough.uninstall_marker"),
    export_path: str = Config("passthrough.export_path"),
    host: Optional[str] = Config("passthrough.export_host"),
):
    """Install the contents of the source directory to a local or remote path."""
    destination = Path(export_path) / corpus
    util.install.install_path(source_dir.source_dir, host, destination)
    marker.write()
    uninstall_marker.remove()


@uninstaller("Passthrough uninstaller")
def uninstall(
    corpus: Corpus = Corpus(),
    marker: OutputMarker = OutputMarker("passthrough.uninstall_marker"),
    install_marker: MarkerOptional = MarkerOptional("passthrough.install_marker"),
    export_path: str = Config("passthrough.export_path"),
    host: Optional[str] = Config("passthrough.export_host"),
):
    """Uninstall the contents of the source directory to a local or remote path."""
    assert corpus and export_path  # Already checked by Sparv
    destination = Path(export_path) / corpus
    util.install.uninstall_path(destination, host)
    marker.write()
    install_marker.remove()
