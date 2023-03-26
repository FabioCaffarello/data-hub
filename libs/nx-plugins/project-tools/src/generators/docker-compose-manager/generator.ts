import {
  formatFiles,
  generateFiles,
  ProjectConfiguration,
  Tree
} from '@nrwl/devkit';
import { readWorkspaceConfig } from '@nrwl/workspace';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import { DockerComposeManagerGeneratorSchema } from './schema';
import { propsMappings, serviceProps, stackMappings } from './stack.services';
import { stackTemplates, networkName } from './template.services';
import { getOwnKeys } from '../../../../utils/json/commands.json'


interface NormalizedSchema extends DockerComposeManagerGeneratorSchema {
  botService: boolean;
  backendService: boolean;
  frontendService: boolean;
  ingestorsObject: {botName: string, botPath: string}[];
  workspacePath: string;
  dockerComposePath: string;
}


const devContainerJsonPath = path.join('.devcontainer', 'devcontainer.json');


function normalizeOptions(tree: Tree, options: DockerComposeManagerGeneratorSchema): NormalizedSchema {
  const { groupServices } = options;
  const workspacePath = getWorkspacePath(tree)
  const dockerComposePath = path.join(workspacePath, 'docker-compose.yml');
  let ingestorsObject: {botName: string, botPath: string}[]

  for (const group of groupServices) {
    const prop = propsMappings[group];
    if (prop) {
      serviceProps[prop] = true;
    } else {
      console.warn(`Unknown group '${group}'`);
    }
  }

  if (serviceProps.botService) {
    ingestorsObject = (options.ingestors ?? '')
    .split(',')
    .map((name) => ({
      botName: `ingestors-${options.coreBusiness}-${options.subjectBusiness}-${name}`,
      botPath: getProjectPath(tree, `ingestors-${options.coreBusiness}-${options.subjectBusiness}-${name}`),
    }));
  }

  return {
    ...options,
    ...serviceProps,
    ingestorsObject,
    workspacePath,
    dockerComposePath
  };
}

function getProjectPath(tree: Tree, projectName: string): string {
  const workspaceConfig = readWorkspaceConfig({
    format: 'nx',
    path: path.join(tree.root, 'workspace.json'),
  });
  const projectConfig: ProjectConfiguration | undefined =
    workspaceConfig.projects[projectName];

  return projectConfig?.root ?? '';
}

function addFiles(tree: Tree, options: NormalizedSchema) {
  const templateOptions = {
    ...options,
    offsetFromRoot: '',
    template: ''
  };
  generateFiles(
    tree,
    path.join(__dirname, 'files'),
    options.workspacePath,
    templateOptions
  );
}

function getWorkspacePath(tree: Tree): string {
  const devContainerJson = JSON.parse(fs.readFileSync(devContainerJsonPath, 'utf-8'));
  const workspaceFolder = devContainerJson['workspaceFolder'];
  if (fs.existsSync(devContainerJsonPath)) {
    if (workspaceFolder.includes(tree.root)) {
      return path.join(tree.root, '..', '..')
    } else {
      return tree.root
    }
  } else {
    return ''
  }
}

function addServices(tree: Tree, options: NormalizedSchema) {
  const dockerComposeContent = tree.read(options.dockerComposePath, 'utf-8');
  const dockerComposeObject = dockerComposeContent
    ? yaml.parse(dockerComposeContent)
    : {};
  const dockerComposeServices = dockerComposeObject.services || {};

  if (options.botService || options.backendService || options.frontendService) {
    // All stacks
    for (const stack of getOwnKeys(stackMappings)) {
      stackMappings[stack].forEach((element) => {
        const stackTemplatesObject = { ...stackTemplates[element] };
        dockerComposeServices[element] = stackTemplatesObject;
      });
    }
    if (options.botService) {
      // Bot Stack
      options.ingestorsObject.forEach((element) => {
        const botServiceObject = {
          build: {
            context: element.botPath,
            dockerfile: 'Dockerfile' // path.join(element.botPath, 'Dockerfile')
          },
          networks: [networkName]
        };
        dockerComposeServices[element.botName] = botServiceObject;
      })
    }
  }
  dockerComposeObject.services = dockerComposeServices;
  const updatedDockerComposeContent = yaml.stringify(dockerComposeObject);
  tree.write(options.dockerComposePath, updatedDockerComposeContent);
}

export default async function (tree: Tree, options: DockerComposeManagerGeneratorSchema) {
  const normalizedOptions = normalizeOptions(tree, options);
  addFiles(tree, normalizedOptions);
  addServices(tree, normalizedOptions);
  await formatFiles(tree);
}
