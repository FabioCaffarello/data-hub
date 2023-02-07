
nx-create-plugin:
	npx nx g @nrwl/nx-plugin:plugin $(pluginName) --directory=nx-plugins

nx-create-plugin-generator:
	npx nx g @nrwl/nx-plugin:generator $(generatorName) --project=$(pluginName)

nx-create-plugin-executor:
	npx nx g @nrwl/nx-plugin:executor $(executorName) --project=$(pluginName)

# npx nx run shared-python-tools-core:add --name shared-python-tools-development --group=dev --local

# docker rm -f $(printf "${$(docker ps -a -q)/$(docker ps --filter=name=data-hub_devcontainer-vscode-1 -q)}" | tr '\n' ' ')

# npx nx generate @data-hub/python-tools:create-project base-parser --description='base parser.' --packageName=base-parser --type=library --directory=ingestors --moduleName=baseparser

# gh act --graph --workflows ./.github/workflows/nx_affected_ci.yaml

# npm install -g npm@9.3.1
# npm install -g cdktf-cli
# cdktf deploy
# cdktf destroy
# install aws toolkit extension and login with iam cred

# npx nx g @nrwl/nx-plugin:executor fix-docker-config --project=

# npx nx run ingestors-financial-mercadobitcoin-tickers:crawler
