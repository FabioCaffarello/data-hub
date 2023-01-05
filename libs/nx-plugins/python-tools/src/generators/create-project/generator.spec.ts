// import { spawnSyncMock } from '../../../../utils/mocks/cross-spawn.mock';
import { createTreeWithEmptyWorkspace } from '@nrwl/devkit/testing';
import { Tree, readProjectConfiguration } from '@nrwl/devkit';

import generator from './generator';
import { CreateProjectGeneratorSchema } from './schema';
// import dedent from "dedent";


// import dedent from 'string-dedent';

describe('create-project generator', () => {
  let appTree: Tree;
  const options: CreateProjectGeneratorSchema = {
    name: 'test',
    type: 'application',
    moduleName: null,
    packageName: 'unittest-test-pkg-name',
  };

  beforeEach(() => {
    appTree = createTreeWithEmptyWorkspace();
  });

  // it('should successfully generate a python project', async () => {
  //   await generator(appTree, options);
  //   const config = readProjectConfiguration(appTree, 'test');
  //   expect(config).toMatchSnapshot();

  //   assertGenerateFiles(appTree, 'apps/test', 'test');
  // });

  it('should generate a python project into a different folder', async () => {
    await generator(appTree, {
      ...options,
      directory: 'shared',
    });
    const config = readProjectConfiguration(appTree, 'shared-test');
    expect(config).toMatchSnapshot();

    assertGenerateFiles(appTree, 'apps/shared/test');
  });

  // it('should successfully generate a python library project with root pyproject.toml', async () => {
  //   appTree.write('pyproject.toml', dedent`
  //   [tool.poetry]
  //   name = "unit test"
  //     [tool.poetry.dependencies]
  //     python = ">=3.8,<3.10"
  //   [build-system]
  //   requires = [ "poetry-core==1.0.3" ]
  //   build-backend = "poetry.core.masonry.api"
  //   `)

  //   const callbackTask = await generator(appTree, { ...options, type: 'library' });
  //   callbackTask();
  //   const config = readProjectConfiguration(appTree, 'test');
  //   expect(config).toMatchSnapshot();

  //   expect(appTree.read('pyproject.toml', 'utf8')).toMatchSnapshot()
  //   expect(spawnSyncMock).toHaveBeenCalledWith('poetry', ['lock'], {
  //     shell: false,
  //     stdio: 'inherit',
  //   });
  // });

  // it('should successfully generate a python project with custom module name', async () => {
  //   await generator(appTree, { ...options, moduleName: 'mymodule' });
  //   const config = readProjectConfiguration(appTree, 'test');
  //   expect(config).toMatchSnapshot();

  //   assertGenerateFiles(appTree, 'apps/test', 'mymodule');
  // });
});


function assertGenerateFiles(
  appTree: Tree,
  projectDirectory: string
) {
  expect(appTree.exists(`${projectDirectory}/README.md`)).toBeTruthy();
}
