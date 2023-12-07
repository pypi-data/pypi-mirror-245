#! /usr/bin/env python

import argparse
import os
import sys
import logging
import logging.config

from cellmaps_utils import logutils
from cellmaps_utils import constants
import cellmaps_coembedding
from cellmaps_coembedding.runner import MuseCoEmbeddingGenerator
from cellmaps_coembedding.runner import FakeCoEmbeddingGenerator
from cellmaps_coembedding.runner import CellmapsCoEmbedder

logger = logging.getLogger(__name__)


PPI_EMBEDDINGDIR='--ppi_embeddingdir'
IMAGE_EMBEDDINGDIR='--image_embeddingdir'

def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: description to display on command line
    :type desc: str
    :param args: command line arguments usually :py:func:`sys.argv[1:]`
    :type args: list
    :return: arguments parsed by :py:mod:`argparse`
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=constants.ArgParseFormatter)
    parser.add_argument('outdir', help='Output directory')
    parser.add_argument(PPI_EMBEDDINGDIR, required=True,
                        help='Directory aka rocrate where ppi '
                             'embedding file resides')
    parser.add_argument(IMAGE_EMBEDDINGDIR, required=True,
                        help='Directory aka rocrate image embedding '
                             'file resides')
    parser.add_argument('--latent_dimension', type=int, default=128,
                        help='Output dimension of embedding')
    parser.add_argument('--n_epochs_init', default=200, type=int,
                        help='# of init training epochs')
    parser.add_argument('--n_epochs', default=500, type=int,
                        help='# of training epochs')
    parser.add_argument('--jackknife_percent', default=0.0, type=float,
                        help='Percentage of data to withhold from training'
                             'a value of 0.1 means to withhold 10 percent of the data')
    parser.add_argument('--fake_embedding', action='store_true',
                        help='If set, generate fake coembeddings')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--skip_logging', action='store_true',
                        help='If set, output.log, error.log '
                             'files will not be created')
    parser.add_argument('--verbose', '-v', action='count', default=1,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = WARNING, -vv = INFO, '
                             '-vvv = DEBUG, -vvvv = NOTSET (default ERROR '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_coembedding.__version__))

    return parser.parse_args(args)


def main(args):
    """
    Main entry point for program

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of :py:meth:`cellmaps_coembedding.runner.CellmapsCoEmbedder.run`
             or ``2`` if an exception is raised
    :rtype: int
    """
    desc = """
    Version {version}

    Given image and PPI embeddings, this tool generates a co-embedding using
    a variant of MuSE algorithm within this code base from
    Feng Bao @ Altschuler & Wu Lab @ UCSF 2022
    that is under MIT License.

    To run this tool requires that an output directory be specified and these
    flags be set.

    {ppi_embeddingdir} should be set to a directory path created by
                       cellmaps_ppi_embedding which has a {ppi_embedding_file} file
                       containing the tab delimited embeddings of the PPI network.
                       For each row, first value is assumed to be the gene symbol
                       followed by the embeddings separated by tabs. The first
                       row is assumed to be a header

    {image_embeddingdir} should be set to a directory path created by
                       cellmaps_image_embedding which has a {image_embedding_file} file
                       containing the tab delimited embeddings of the IF images
                       For each row, first value is assumed to be sample ID followed
                       by the embeddings separated by tabs. The first row
                       is assumed to be a header.

    """.format(version=cellmaps_coembedding.__version__,
               ppi_embeddingdir=PPI_EMBEDDINGDIR,
               image_embeddingdir=IMAGE_EMBEDDINGDIR,
               ppi_embedding_file=constants.PPI_EMBEDDING_FILE,
               image_embedding_file=constants.IMAGE_EMBEDDING_FILE,
               image_gene_node_attr_file=constants.IMAGE_GENE_NODE_ATTR_FILE)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_coembedding.__version__

    try:
        logutils.setup_cmd_logging(theargs)
        if theargs.fake_embedding:
            gen = FakeCoEmbeddingGenerator(dimensions=theargs.latent_dimension,
                                           ppi_embeddingdir=theargs.ppi_embeddingdir,
                                           image_embeddingdir=theargs.image_embeddingdir)
        else:
            gen = MuseCoEmbeddingGenerator(dimensions=theargs.latent_dimension,
                                           n_epochs=theargs.n_epochs,
                                           n_epochs_init=theargs.n_epochs_init,
                                           jackknife_percent=theargs.jackknife_percent,
                                           outdir=os.path.abspath(theargs.outdir),
                                           ppi_embeddingdir=theargs.ppi_embeddingdir,
                                           image_embeddingdir=theargs.image_embeddingdir)
        return CellmapsCoEmbedder(outdir=theargs.outdir,
                                  inputdirs=[theargs.image_embeddingdir, theargs.ppi_embeddingdir],
                                  embedding_generator=gen,
                                  skip_logging=theargs.skip_logging,
                                  input_data_dict=theargs.__dict__).run()
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
