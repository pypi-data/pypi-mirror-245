from abc import ABC
from abc import abstractmethod
from logging import Logger
from pathlib import Path
from typing import Generator

from easy_logs import get_logger
from rich.progress import track
from rich.status import Status
from stockfish import Stockfish

from chess_insight.game import Game

logger = get_logger()


class ApiCommunicator(ABC):
    HOST: str = None

    def __init__(self, stockfish_path: Path = "stockfish.exe", depth: int = 10) -> None:
        """
        Summary:
            Abstract class for API communication. It is used to get games from chess.com, lichess, etc.
            Each subclass should implement get_games method.
        Args:
            logger (Logger): logger to log to
            depth (int, optional): depth of stockfish engine. Defaults to 10.
        """
        if not stockfish_path or not Path(stockfish_path).exists():
            logger.warning(
                f"Stockfish does not exists in given path {stockfish_path}. Therefore won't be used."
            )
            self.stockfish = None
            return
        try:
            stockfish_path = Path(stockfish_path).resolve()
            self.stockfish = Stockfish(stockfish_path.resolve(), depth=depth)
        except (AttributeError, FileNotFoundError) as err:
            raise err

    def split_pgns(self, text_pgn: str) -> list[str]:
        """
        Summary:
            Splits pgn string into list of pgn strings.
        Args:
            text_pgn (str): pgn string to split
        Returns:
            list of pgn strings
        """
        pgns = text_pgn.split("\n\n\n")
        while pgns and len(pgns[-1]) == 0:
            pgns.pop()
        return pgns

    def games_generator(
        self, username: str, count: int, time_class: str
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            list_of_pgns (int): number of pgn strings to compute
        returns:
            generator of Game objects, each representing a game played on chess.com
        """
        logger.info(f"Collecting games for {username} from {self.HOST}")
        list_of_pgns = self.get_pgns(username, count, time_class)
        logger.info(f"Collected {len(list_of_pgns)} games")
        logger.info(f"Collected {len(list_of_pgns)} games")
        progress = track(
            list_of_pgns,
            description=f"Analyzing games for {username}\n",
            total=len(list_of_pgns),
            transient=True,
        )
        for game in progress:
            game = Game(
                game,
                username,
                stockfish=self.stockfish,
            )
            yield game

    @abstractmethod
    def get_pgns(
        self, username: str, number_of_games: int, time_class: str
    ) -> Generator[Game, None, None]:
        """
        Args:
            username (str): username on given portal (lichess, chess.com, etc.) to get games from
            games (int): number of lastest games to get
            time_class (_type_): time class of games to get (blitz, rapid, bullet, daily)
        returns:
            generator of Game objects, each representing a game played on chess.com, licess, etc.
        """
