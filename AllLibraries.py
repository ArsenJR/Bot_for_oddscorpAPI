import sys
import time
import json
import requests
import logging
from time import sleep
from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QItemSelectionModel, Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QPushButton

import math

logging.basicConfig(format="%(message)s", level=logging.INFO)