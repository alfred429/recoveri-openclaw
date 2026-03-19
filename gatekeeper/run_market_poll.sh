#!/bin/bash
# Market Data Poller — Cron wrapper
# Loads env vars and runs the poller
# Sprint 9 | Session 12

export $(grep -v '^#' /root/.env | xargs)
cd /root/gatekeeper
python3 market_poller.py >> /root/shared-repository/data/market-intel/cron.log 2>&1
