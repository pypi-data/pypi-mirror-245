#!/usr/bin/env python3
import imgdups

SEARCH_PATH = "search"
TARGET_PATH = "target"

img_dups = imgdups.ImgDups(TARGET_PATH, SEARCH_PATH)
img_dups.find_duplicates()
