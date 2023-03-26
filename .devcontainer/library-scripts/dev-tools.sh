#!/usr/bin/env bash
# export $(cat .env)

npm install
npm install -g npm@9.5.0 cdktf-cli @backstage/cli yarn
npm install --save @backstage/plugin-catalog-backend @backstage/plugin-catalog
poetry install

export CGO_ENABLED=1

# gh extension install nektos/gh-act
# npx nx generate @data-hub/project-tools:fix-docker-config
