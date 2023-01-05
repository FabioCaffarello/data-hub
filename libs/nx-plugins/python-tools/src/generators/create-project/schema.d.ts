export interface CreateProjectGeneratorSchema {
    name: string;
    tags?: string;
    type: 'library' | 'application';
    directory?: string;
    // moduleName: string;
    packageName: string;
    description: string;
    // authors: string;
}
