"""SBX specific annotation and export functions related to the stats export."""
import os
from typing import Optional

from sparv.api import (
    AllSourceFilenames,
    Annotation,
    AnnotationAllSourceFiles,
    Config,
    Corpus,
    Export,
    ExportInput,
    MarkerOptional,
    Output,
    OutputMarker,
    annotator,
    exporter,
    get_logger,
    installer,
    uninstaller,
    util
)
from .stats_export import freq_list

logger = get_logger(__name__)


@annotator("Extract the complemgram with the highest score", language=["swe"])
def best_complemgram(
        out: Output = Output("<token>:stats_export.complemgram_best", description="Complemgram annotation with highest score"),
        complemgram: Annotation = Annotation("<token>:saldo.complemgram")):
    """Extract the complemgram with the highest score."""
    from sparv.modules.misc import misc
    misc.best_from_set(out, complemgram, is_sorted=True)


@annotator("Extract the sense with the highest score", language=["swe"])
def best_sense(
        out: Output = Output("<token>:stats_export.sense_best", description="Sense annotation with highest score"),
        sense: Annotation = Annotation("<token>:wsd.sense")):
    """Extract the sense annotation with the highest score."""
    from sparv.modules.misc import misc
    misc.best_from_set(out, sense, is_sorted=True)


@annotator("Extract the first baseform annotation from a set of baseforms", language=["swe"])
def first_baseform(
        out: Output = Output("<token>:stats_export.baseform_first", description="First baseform from a set of baseforms"),
        baseform: Annotation = Annotation("<token:baseform>")):
    """Extract the first baseform annotation from a set of baseforms."""
    from sparv.modules.misc import misc
    misc.first_from_set(out, baseform)


@annotator("Extract the first lemgram annotation from a set of lemgrams", language=["swe"])
def first_lemgram(
        out: Output = Output("<token>:stats_export.lemgram_first", description="First lemgram from a set of lemgrams"),
        lemgram: Annotation = Annotation("<token>:saldo.lemgram")):
    """Extract the first lemgram annotation from a set of lemgrams."""
    from sparv.modules.misc import misc
    misc.first_from_set(out, lemgram)


@annotator("Get the best complemgram if the token is lacking a sense annotation", language=["swe"])
def conditional_best_complemgram(
    out_complemgrams: Output = Output("<token>:stats_export.complemgram_best_cond",
                                      description="Compound analysis using lemgrams"),
    complemgrams: Annotation= Annotation("<token>:stats_export.complemgram_best"),
    sense: Annotation = Annotation("<token:sense>")):
    """Get the best complemgram if the token is lacking a sense annotation."""
    all_annotations = list(complemgrams.read_attributes((complemgrams, sense)))
    short_complemgrams = []
    for complemgram, sense in all_annotations:
        if sense and sense != "|":
            complemgram = ""
        short_complemgrams.append(complemgram)
    out_complemgrams.write(short_complemgrams)


@exporter("Corpus word frequency list", language=["swe"], order=1)
def sbx_freq_list(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    msd: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:msd>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.baseform_first"),
    sense: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.sense_best"),
    lemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.lemgram_first"),
    complemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles(
                                            "<token>:stats_export.complemgram_best_cond"),
    out: Export = Export("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for the entire corpus.

    Args:
        source_files: The source files belonging to this corpus.
        word: Word annotations.
        token: Token span annotations.
        msd: MSD annotations.
        baseform: Annotations with first baseform from each set.
        sense: Best sense annotations.
        lemgram: Annotations with first lemgram from each set.
        complemgram: Conditional best compound lemgram annotations.
        out: The output word frequency file.
        delimiter: Column delimiter to use in the csv.
        cutoff: The minimum frequency a word must have in order to be included in the result.
    """
    annotations = [(word, "token"), (msd, "POS"), (baseform, "lemma"), (sense, "SALDO sense"), (lemgram, "lemgram"),
                   (complemgram, "compound")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@exporter("Corpus word frequency list", language=["swe"])
def sbx_freq_list_date(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    msd: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:msd>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.baseform_first"),
    sense: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.sense_best"),
    lemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.lemgram_first"),
    complemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles(
                                            "<token>:stats_export.complemgram_best_cond"),
    date: AnnotationAllSourceFiles = AnnotationAllSourceFiles("[dateformat.out_annotation]:dateformat.date_pretty"),
    out: Export = Export("stats_export.frequency_list_sbx_date/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for the entire corpus.

    Args:
        source_files: The source files belonging to this corpus.
        word: Word annotations.
        token: Token span annotations.
        msd: MSD annotations.
        baseform: Annotations with first baseform from each set.
        sense: Best sense annotations.
        lemgram: Annotations with first lemgram from each set.
        complemgram: Conditional best compound lemgram annotations.
        date: date annotation
        out: The output word frequency file.
        delimiter: Column delimiter to use in the csv.
        cutoff: The minimum frequency a word must have in order to be included in the result.
    """
    annotations = [(word, "token"), (msd, "POS"), (baseform, "lemma"), (sense, "SALDO sense"), (lemgram, "lemgram"),
                   (complemgram, "compound"), (date, "date")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@exporter("Corpus word frequency list (without Swedish annotations)", language=["swe"], order=2)
def sbx_freq_list_simple_swe(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    pos: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:pos>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.baseform_first"),
    out: Export = Export("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for a corpus without sense, lemgram and complemgram annotations."""
    annotations = [(word, "token"), (pos, "POS"), (baseform, "lemma")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@exporter("Corpus word frequency list (without Swedish annotations)", order=3)
def sbx_freq_list_simple(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    pos: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:pos>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:baseform>"),
    out: Export = Export("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for a corpus without sense, lemgram and complemgram annotations."""
    annotations = [(word, "token"), (pos, "POS"), (baseform, "lemma")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@exporter("Corpus word frequency list for Swedish from the 1800's", language=["swe-1800"], order=4)
def sbx_freq_list_1800(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    msd: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:msd>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.baseform_first"),
    sense: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:hist.sense"),
    lemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>:stats_export.lemgram_first"),
    complemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles(
                                            "<token>:stats_export.complemgram_best_cond"),
    out: Export = Export("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for the entire corpus."""

    annotations = [(word, "token"), (msd, "POS"), (baseform, "lemma"), (sense, "SALDO sense"), (lemgram, "lemgram"),
                   (complemgram, "compound")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@exporter("Corpus word frequency list for Old Swedish (without part-of-speech)", language=["swe-fsv"], order=5)
def sbx_freq_list_fsv(
    source_files: AllSourceFilenames = AllSourceFilenames(),
    token: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token>"),
    word: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:word>"),
    baseform: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:baseform>"),
    lemgram: AnnotationAllSourceFiles = AnnotationAllSourceFiles("<token:lemgram>"),
    out: Export = Export("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    delimiter: str = Config("stats_export.delimiter"),
    cutoff: int = Config("stats_export.cutoff")):
    """Create a word frequency list for a corpus without sense, lemgram and complemgram annotations."""
    annotations = [(word, "token"), (baseform, "lemma"), (lemgram, "lemgram")]

    freq_list(source_files=source_files, word=word, token=token, annotations=annotations, source_annotations=[],
              out=out, sparv_namespace="", source_namespace="", delimiter=delimiter, cutoff=cutoff)


@installer("Install SBX word frequency list on remote host", uninstaller="stats_export:uninstall_sbx_freq_list")
def install_sbx_freq_list(
    freq_list: ExportInput = ExportInput("stats_export.frequency_list_sbx/stats_[metadata.id].csv"),
    marker: OutputMarker = OutputMarker("stats_export.install_sbx_freq_list_marker"),
    uninstall_marker: MarkerOptional = MarkerOptional("stats_export.uninstall_sbx_freq_list_marker"),
    host: Optional[str] = Config("stats_export.remote_host"),
    target_dir: str = Config("stats_export.remote_dir")
):
    """Install frequency list on server by rsyncing."""
    util.install.install_path(freq_list, host, target_dir)
    uninstall_marker.remove()
    marker.write()


@installer("Install SBX word frequency list with dates on remote host",
           uninstaller="stats_export:uninstall_sbx_freq_list_date")
def install_sbx_freq_list_date(
    freq_list: ExportInput = ExportInput("stats_export.frequency_list_sbx_date/stats_[metadata.id].csv"),
    marker: OutputMarker = OutputMarker("stats_export.install_sbx_freq_list_date_marker"),
    uninstall_marker: MarkerOptional = MarkerOptional("stats_export.uninstall_sbx_freq_list_date_marker"),
    host: Optional[str] = Config("stats_export.remote_host"),
    target_dir: str = Config("stats_export.remote_dir")
):
    """Install frequency list on server by rsyncing."""
    util.install.install_path(freq_list, host, target_dir)
    uninstall_marker.remove()
    marker.write()


@uninstaller("Uninstall SBX word frequency list")
def uninstall_sbx_freq_list(
    corpus_id: Corpus = Corpus(),
    marker: OutputMarker = OutputMarker("stats_export.uninstall_sbx_freq_list_marker"),
    install_marker: MarkerOptional = MarkerOptional("stats_export.install_sbx_freq_list_marker"),
    host: Optional[str] = Config("stats_export.remote_host"),
    remote_dir: str = Config("stats_export.remote_dir")
):
    """Uninstall SBX word frequency list."""
    remote_file = os.path.join(remote_dir, f"stats_{corpus_id}.csv")
    logger.info("Removing SBX word frequency file %s%s", host + ":" if host else "", remote_file)
    util.install.uninstall_path(remote_file, host)
    install_marker.remove()
    marker.write()


@uninstaller("Uninstall SBX word frequency list with dates")
def uninstall_sbx_freq_list_date(
    corpus_id: Corpus = Corpus(),
    marker: OutputMarker = OutputMarker("stats_export.uninstall_sbx_freq_list_date_marker"),
    install_marker: MarkerOptional = MarkerOptional("stats_export.install_sbx_freq_list_date_marker"),
    host: Optional[str] = Config("stats_export.remote_host"),
    remote_dir: str = Config("stats_export.remote_dir")
):
    """Uninstall SBX word frequency list with dates."""
    remote_file = os.path.join(remote_dir, f"stats_{corpus_id}.csv")
    logger.info("Removing SBX word frequency with dates file %s%s", host + ":" if host else "", remote_file)
    util.install.uninstall_path(remote_file, host)
    install_marker.remove()
    marker.write()
