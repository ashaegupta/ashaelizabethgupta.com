#!/bin/bash

echo 'updating project data...'
python project_data.py
echo 'rendering templates...'
python render.py
