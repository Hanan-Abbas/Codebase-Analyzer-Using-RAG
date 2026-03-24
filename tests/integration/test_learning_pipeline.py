import pytest
import sqlite3
import os
from unittest.mock import MagicMock
from src.services.learning_service.feedback_collector import FeedbackCollector
from src.services.learning_service.optimizer import RankingOptimizer