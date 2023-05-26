import {
  Tree,
} from '@nrwl/devkit';
import { createTreeWithEmptyWorkspace } from '@nrwl/devkit/testing';
import generator from './generator';
import { DockerComposeManagerGeneratorSchema } from './schema';

describe('docker-compose-manager generator', () => {
  let appTree: Tree;
  const options: DockerComposeManagerGeneratorSchema = {
    groupServices: ['bot'],
    coreBusiness: 'financial',
    subjectBusiness: 'mercadobitcoin',
    ingestors: 'tickers',
  };

  beforeEach(() => {
    appTree = createTreeWithEmptyWorkspace({layout: 'apps-libs'});
  });

  it('should generate a docker-compose file', async () => {
    await generator(appTree, options);
    assertGenerateFiles(appTree);

  });
});

function assertGenerateFiles(
  appTree: Tree,
) {
  expect(appTree.exists(`${appTree.root}/docker-compose.yml`)).toBeTruthy();
  expect(
    appTree.read(`${appTree.root}/docker-compose.yml`).toString()
  ).toMatchSnapshot();
}
