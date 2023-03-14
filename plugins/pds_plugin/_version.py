# GNU Lesser General Public License v3  for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pds-crawler.  If not, see <https://www.gnu.org/licenses/>.
# pds-crawler - ETL to index PDS data to pdssp
# Copyright (C) 2023 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
# This file is part of pds-crawler <https://github.com/pdssp/pdsp-airflow>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Project metadata."""
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

__name_soft__ = "pdsp-airflow"
try:
    __version__ = get_distribution(__name_soft__).version
except DistributionNotFound:
    __version__ = "0.0.0"
__title__ = "pdsp-airflow"
__description__ = """Workflow manager for the PDSSP platform"""
__url__ = "https://github.com/pdssp/pdsp-airflow"
__author__ = "Jean-Christophe Malapert"
__author_email__ = "jean-christophe.malapert@cnes.fr"
__license__ = "GNU Lesser General Public License v3"
__copyright__ = (
    "2023, CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)"
)