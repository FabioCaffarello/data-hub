import { execSync } from 'child_process';

export function getCurrentGitUserName() {
  try {
    return execSync(`git config --get user.name`).toString('utf-8').trim()
  } catch {
    return ''
  }
}

export function getCurrentGitUserEmail() {
  try {
    return execSync(`git config --get user.email`).toString('utf-8').trim()
  } catch {
    return ''
  }
}
