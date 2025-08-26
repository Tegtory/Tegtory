import logging

from tegtory.domain.queries.base import BaseQuery
from tegtory.domain.results import Failure, Success
from tegtory.domain.use_cases.queries.base import BaseQueryHandler
from tegtory.infrastructure.executor import BaseExecutor

logger = logging.getLogger(__name__)


class QueryExecutor(BaseExecutor):
    handler_base_class = BaseQueryHandler

    async def ask(self, query: BaseQuery) -> Success | Failure:
        logger.info(f"Executing query: {query.__class__.__name__}({query})")
        return await self.handlers[type(query)](query)
