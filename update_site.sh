#!/bin/bash

echo 'updating data...'
python project_data.py

echo 'rendering templates...'
python render.py

echo 'done.'
