#!/bin/bash
echo "Start script"

flask db migrate

flask db upgrade

flask category_load