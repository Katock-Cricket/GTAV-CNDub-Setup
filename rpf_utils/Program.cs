using CodeWalker.GameFiles;
using System;
using System.IO;

namespace RpfUtilsLib
{
    public static class RpfUtils
    {
        public static string[] ImportFilesToRpf(
            string rpfPath,
            string innerPath,
            string gtaFolder,
            bool isGen9,
            string[] filesToImport)
        {
            var logs = new System.Collections.Generic.List<string>();

            try
            {
                GTA5Keys.LoadFromPath(gtaFolder, isGen9, null);
                logs.Add("GTA5Keys loaded.");

                var rootRpf = new RpfFile(rpfPath, "");
                rootRpf.ScanStructure(
                    status => logs.Add($"[Status] {status}"),
                    error => logs.Add($"[Error] {error}")
                );
                RpfDirectoryEntry entry = null;
                if (innerPath == "")
                {
                    entry = rootRpf.Root;
                }
                else
                {
                    entry = FindEntry(rootRpf, innerPath, logs);
                }
                if (entry == null)
                {
                    logs.Add("Inner directory not found.");
                    return logs.ToArray();
                }

                foreach (var fpath in filesToImport)
                {
                    if (!File.Exists(fpath))
                    {
                        logs.Add($"File not found: {fpath}");
                        continue;
                    }

                    var fi = new FileInfo(fpath);
                    if (fi.Length > 0x3FFFFFFF)
                    {
                        logs.Add($"File too large: {fpath}");
                        continue;
                    }

                    byte[] data = File.ReadAllBytes(fpath);
                    rootRpf.Encryption = RpfEncryption.OPEN;
                    var newFile = RpfFile.CreateFile(entry, fi.Name, data);
                    logs.Add($"Imported {newFile.ToString()} to {entry.ToString()}");
                }
            }
            catch (Exception ex)
            {
                logs.Add($"Exception: {ex}");
            }

            return logs.ToArray();
        }

        private static RpfDirectoryEntry FindEntry(RpfFile rootRpf, string path, System.Collections.Generic.List<string> logs)
        {
            path = path.Replace('/', '\\');
            var parts = path.Split(new[] { '\\', '/' }, StringSplitOptions.RemoveEmptyEntries);
            RpfDirectoryEntry curDir = rootRpf.Root;
            if (curDir == null)
            {
                logs.Add("Root directory not found.");
                return null;
            }

            foreach (var part in parts)
            {
                if (curDir == null)
                {
                    logs.Add($"Directory not found at part: {part}");
                    return null;
                }

                if (part.EndsWith(".rpf", StringComparison.OrdinalIgnoreCase))
                {
                    logs.Add("Found RPF file: " + part);
                    logs.Add("Path: " + path);
                    foreach (var entry in rootRpf.AllEntries)
                    {
                        logs.Add(entry.Name);
                        logs.Add(entry.Path);
                        if (entry is RpfFileEntry fileEntry &&
                            entry.Name.Equals(part, StringComparison.OrdinalIgnoreCase) &&
                            entry.Path.EndsWith(path, StringComparison.OrdinalIgnoreCase))
                        {
                            var childRpf = rootRpf.FindChildArchive(fileEntry);
                            if (childRpf != null)
                            {
                                curDir = childRpf.Root;
                                logs.Add($"Entered child RPF: {childRpf.Name}");
                            }
                            break;
                        }
                    }
                }
                else
                {
                    curDir = curDir.Directories.Find(d =>
                        d.NameLower.Equals(part.ToLowerInvariant()));
                }

                if (curDir == null)
                {
                    logs.Add($"Subdirectory not found: {part}");
                    return null;
                }
            }

            return curDir;
        }
    }
}