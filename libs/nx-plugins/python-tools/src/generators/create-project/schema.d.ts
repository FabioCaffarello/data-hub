export interface CreateProjectGeneratorSchema {
  name: string;
  tags?: string;
  type: 'library' | 'application';
  directory?: string;
  packageName: string;
  moduleName: string;
  description?: string;
}
