
nx-create-plugin:
	npx nx g @nrwl/nx-plugin:plugin $(pluginName) --directory=nx-plugins --importPath=@data-hub/$(pluginName)

nx-create-plugin-generator:
	npx nx g @nrwl/nx-plugin:generator $(generatorName) --project=$(pluginName)

# npx nx run shared-python-tools-core:add --name shared-python-tools-development --group=dev --local

# docker rm -f $(printf "${$(docker ps -a -q)/$(docker ps --filter=name=data-hub_devcontainer-vscode-1 -q)}" | tr '\n' ' ')


# gh act --graph --workflows ./.github/workflows/nx_affected_ci.yaml
