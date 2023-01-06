import { spawnSyncMock } from '../../../../utils/mocks/cross-spawn.mock';
import { readProjectConfiguration, Tree } from '@nrwl/devkit';
import { createTreeWithEmptyWorkspace } from '@nrwl/devkit/testing';

import generator from './generator';
import { CreateProjectGeneratorSchema } from './schema';
import dedent from "dedent";


describe('create-project generator', () => {
  let appTree: Tree;
  const options: CreateProjectGeneratorSchema = {
    name: 'test',
    type: 'application',
    moduleName: null,
    packageName: 'unittest-test-pkg-name',
  };

  beforeEach(() => {
    appTree = createTreeWithEmptyWorkspace({layout: 'apps-libs'});
  });

  it('should successfully generate a python project', async () => {
    await generator(appTree, options);
    const config = readProjectConfiguration(appTree, 'test');
    expect(config).toMatchSnapshot();

    assertGenerateFiles(appTree, 'apps/test', 'test');
  });

  it('should successfully generate a python project with custom module name', async () => {
    await generator(appTree, { ...options, moduleName: 'mymodule' });
    const config = readProjectConfiguration(appTree, 'test');
    expect(config).toMatchSnapshot();

    assertGenerateFiles(appTree, 'apps/test', 'mymodule');
  });

  it('should successfully generate a python library project', async () => {
    await generator(appTree, { ...options, type: 'library' });
    const config = readProjectConfiguration(appTree, 'test');
    expect(config).toMatchSnapshot();

    assertGenerateFiles(appTree, 'libs/test', 'test');
  });

  it('should generate a python project into a different folder', async () => {
    await generator(appTree, {
      ...options,
      directory: 'shared',
    });
    const config = readProjectConfiguration(appTree, 'shared-test');
    expect(config).toMatchSnapshot();

    assertGenerateFiles(appTree, 'apps/shared/test', 'shared_test');
  });

  it('should generate a python project using description option', async () => {
    await generator(appTree, {
      ...options,
      description: 'My custom description',
    });
    expect(
      appTree.read('apps/test/pyproject.toml').toString()
    ).toMatchSnapshot();
  });

  it('should generate a python project with tags', async () => {
    await generator(appTree, {
      ...options,
      tags: 'python-project, nx, poetry, tox',
    });
    const config = readProjectConfiguration(appTree, 'test');
    expect(config).toMatchSnapshot();
  });

  it('should successfully generate a python library project with root pyproject.toml', async () => {
    appTree.write('pyproject.toml', dedent`
    [tool.poetry]
    name = "unit test"
      [tool.poetry.dependencies]
      python = ">=3.8,<3.10"
    [build-system]
    requires = [ "poetry-core==1.1.0b3" ]
    build-backend = "poetry.core.masonry.api"
    `)

    const callbackTask = await generator(appTree, { ...options, type: 'library' });
    callbackTask();
    const config = readProjectConfiguration(appTree, 'test');
    expect(config).toMatchSnapshot();

    expect(appTree.read('pyproject.toml', 'utf8')).toMatchSnapshot()
    expect(spawnSyncMock).toHaveBeenCalledWith('poetry', ['update', options.packageName], {
      shell: false,
      stdio: 'inherit',
    });
  });
});


function assertGenerateFiles(
  appTree: Tree,
  projectDirectory: string,
  moduleName: string
) {
  expect(appTree.exists(`${projectDirectory}/README.md`)).toBeTruthy();
  expect(
    appTree.read(`${projectDirectory}/README.md`).toString()
  ).toMatchSnapshot();
  expect(appTree.exists(`${projectDirectory}/pyproject.toml`)).toBeTruthy();
  expect(
    appTree.read(`${projectDirectory}/pyproject.toml`).toString()
  ).toMatchSnapshot();
  expect(appTree.exists(`${projectDirectory}/CHANGELOG.md`)).toBeTruthy();
  expect(
    appTree.read(`${projectDirectory}/CHANGELOG.md`).toString()
  ).toMatchSnapshot();
  expect(
    appTree.exists(`${projectDirectory}/${moduleName}/__init__.py`)
  ).toBeTruthy();
  expect(
    appTree.read(`${projectDirectory}/${moduleName}/__init__.py`).toString()
  ).toMatchSnapshot();
}
