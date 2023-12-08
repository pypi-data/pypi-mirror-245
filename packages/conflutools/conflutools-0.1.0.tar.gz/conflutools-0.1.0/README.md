# Atlassian Confluence Tools

## Generic Setup

```bash
pip install conflutools

# copy the confluence-configuration file and adjust its content:
cp confconf-example.yaml confconf.yaml
vim confconf.yaml
```

## Recursive page export

After the preparation steps above:

```bash
# create a directory for storing the exports:
$EXPORT_DIR="/path/for/storing/wiki-exports"
mkdir $EXPORT_DIR
cd $EXPORT_DIR

# export by page ID:
export-pagetree --config confconf.yaml --page 53838601

# export by page title (requires the space KEY as well):
export-pagetree --config confconf.yaml --page "Project XY Pages" --space "FOO"
```
