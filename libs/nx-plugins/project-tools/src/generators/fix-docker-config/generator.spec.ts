import { createTreeWithEmptyWorkspace } from '@nrwl/devkit/testing';
import { assertGenerateFiles } from './generator';
import { FixDockerConfigGeneratorSchema } from './schema';
import generator from './generator';

describe('fix-docker-config generator', () => {
  let appTree;
  const options: FixDockerConfigGeneratorSchema = {};

  beforeEach(() => {
    appTree = createTreeWithEmptyWorkspace();
  });

  it('should remove the credsStore field from the .docker/config.json file', async () => {
    appTree.write('.docker/config.json', '{"credsStore":"someCredsStore"}');
    await generator(appTree, options);
    assertGenerateFiles(appTree);
  });
});
