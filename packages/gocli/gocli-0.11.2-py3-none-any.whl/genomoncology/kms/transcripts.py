import logging

from cytoolz.curried import curry

import gosdk

_logger = logging.getLogger(__name__)


@curry
def process_transcript_batch(data):
    batch = [
        "%s|%s|%s" % (record["chromosome"], record["start"], record["end"])
        for record in data
    ]
    _logger.debug("get_transcripts_batch: batch=%s", batch)

    results = gosdk.call_with_retry(
        gosdk.sdk.region_search.region_search_batch,
        batch=batch
    )
    return results


@curry
def process_transcript_batch_get_genes(data):
    batch = [
        "%s|%s|%s" % (record["chromosome"], record["start"], record["end"])
        for record in data
    ]
    _logger.debug("get_transcripts_batch: batch=%s", batch)
    # Get all regions for the genes
    results = gosdk.call_with_retry(
        gosdk.sdk.region_search.region_search_batch,
        batch=batch
    )
    # we only need the gene names from the result that is returned,
    # We also do not want duplicate names.
    list_of_genes = []
    for line in results:
        transcripts = line.get("transcripts", [])
        for transcript in transcripts:
            list_of_genes.append(transcript.get("gene"))
    return set(list_of_genes)
