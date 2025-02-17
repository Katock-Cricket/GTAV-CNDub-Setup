import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const src = path.resolve(__dirname, 'dist');
const dest = path.resolve(__dirname, '../Assets/UI');

fs.copy(src, dest)
  .then(() => console.log('拷贝完成!'))
  .catch(err => console.error(err));
