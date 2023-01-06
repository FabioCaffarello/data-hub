import {
  addProjectConfiguration,
  formatFiles,
  generateFiles,
  getWorkspaceLayout,
  names,
  offsetFromRoot,
  Tree,
} from '@nrwl/devkit';
import * as path from 'path';
import { PyprojectToml } from '@nxlv/python'
import { parse, stringify } from '@iarna/toml';
import { CreateProjectGeneratorSchema } from './schema';
import spawn from 'cross-spawn';

interface NormalizedSchema extends CreateProjectGeneratorSchema {
  projectName: string;
  projectRoot: string;
  projectDirectory: string;
  parsedTags: string[];
  moduleName: string;
}

function normalizeOptions(tree: Tree, options: CreateProjectGeneratorSchema): NormalizedSchema {
  const name = names(options.name).fileName;
  const projectDirectory = options.directory
    ? `${names(options.directory).fileName}/${name}`
    : name;
  const projectName = projectDirectory.replace(new RegExp('/', 'g'), '-');
  const moduleName = options.moduleName ? options.moduleName : projectName.replace(new RegExp('-', 'g'), '_');

  let projectRoot = '';
  if (options.type === 'application') {
    projectRoot = `${getWorkspaceLayout(tree).appsDir}/${projectDirectory}`;
  } else {
    projectRoot = `${getWorkspaceLayout(tree).libsDir}/${projectDirectory}`;
  }
  const parsedTags = options.tags
    ? options.tags.split(',').map((s) => s.trim())
    : [];

  return {
    ...options,
    description: options.description ?? '',
    projectName,
    projectRoot,
    projectDirectory,
    parsedTags,
    moduleName,
  };
}

function addFiles(tree: Tree, options: NormalizedSchema) {
    const templateOptions = {
      ...options,
      ...names(options.name),
      offsetFromRoot: offsetFromRoot(options.projectRoot),
      template: ''
    };
    generateFiles(tree, path.join(__dirname, 'files'), options.projectRoot, templateOptions);
}

function updateRootPyprojectToml(
  tree: Tree,
  normalizedOptions: NormalizedSchema
) {
  if (tree.exists('./pyproject.toml')) {
    const rootPyprojectToml = parse(
      tree.read('pyproject.toml', 'utf-8')
    ) as PyprojectToml;
    rootPyprojectToml.tool.poetry.dependencies[normalizedOptions.packageName] =
      {
        path: normalizedOptions.projectRoot,
        develop: true,
      };
      tree.write('pyproject.toml', stringify(rootPyprojectToml));
  }
}

function updateRootPoetryLock(tree: Tree, normalizedOptions: NormalizedSchema) {
  if (tree.exists('./pyproject.toml')) {
    console.log(`Updating root poetry.lock...`);
    const executable = 'poetry';
    const updateArgs = ['update', normalizedOptions.packageName];
    spawn.sync(executable, updateArgs, {
      shell: false,
      stdio: 'inherit',
    });
    return executable
  }
}
async function generator(tree: Tree, options: CreateProjectGeneratorSchema) {
  const normalizedOptions = normalizeOptions(tree, options);
  addProjectConfiguration(
    tree,
    normalizedOptions.projectName,
    {
      root: normalizedOptions.projectRoot,
      projectType: normalizedOptions.type,
      sourceRoot: `${normalizedOptions.projectRoot}/${normalizedOptions.moduleName}`,
      targets: {
        lock: {
          executor: '@nrwl/workspace:run-commands',
          options: {
            command: 'poetry lock --no-update',
            cwd: normalizedOptions.projectRoot,
          },
        },
        add: {
          executor: '@nxlv/python:add',
          options: {},
        },
        update: {
          executor: '@nxlv/python:update',
          options: {},
        },
        remove: {
          executor: '@nxlv/python:remove',
          options: {},
        },
        install: {
          executor: '@nxlv/python:install',
          options: {
            silent: false,
            args: '',
            cacheDir: `.cache/pypoetry`,
            verbose: false,
            debug: false,
          },
        }
      },
      tags: normalizedOptions.parsedTags,
    }
  );
  addFiles(tree, normalizedOptions);
  updateRootPyprojectToml(tree, normalizedOptions);
  await formatFiles(tree);

  return () => {
    updateRootPoetryLock(tree, normalizedOptions);
  };
}

export default generator;
