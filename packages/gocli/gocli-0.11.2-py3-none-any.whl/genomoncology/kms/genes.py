from functools import partial

from cytoolz.curried import curry
from genomoncology.cli.const import GRCH37
from genomoncology.parse.doctypes import DocType
from genomoncology.parse.ensures import ensure_collection
from genomoncology.pipeline.converters import obj_to_dict

import gosdk


@curry
def genes(data, fields=("chromosome", "start", "end", "name")):
    batch = ensure_collection(data)
    gene_list = gosdk.call_with_retry(
        gosdk.sdk.genes.get_genes,
        name=batch,
        fields=fields,
        page_size=len(batch)
    )
    func = partial(obj_to_dict, fields, __type__=DocType.GENE.value)
    return list(map(func, gene_list))


@curry
def boundaries(
    data, fields=("chromosome", "start", "end", "gene"), build=GRCH37
):
    batch = ensure_collection(data)
    gene_list = gosdk.call_with_retry(
        gosdk.sdk.genes.gene_boundaries,
        name=batch,
        build=build
    )
    func = partial(obj_to_dict, fields, __type__=DocType.GENE.value)
    formatted_results = list(map(func, gene_list))
    if gene_list.not_found:
        formatted_results.append("The following genes could not be found: {}".format(
            ", ".join(gene_list.not_found)))
    return formatted_results
