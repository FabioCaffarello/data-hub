#!/usr/bin/env bash
export $(cat .env)

npm install
npm install -g npm@9.3.1 cdktf-cli
poetry install

gh extension install nektos/gh-act
npx nx generate @data-hub/project-tools:fix-docker-config