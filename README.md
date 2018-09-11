# LUMEN TRIGGER UPDATE
Updating Lumen Dataset within Dataset ID `https://<instance_id>.akvolumen.org/api/<dataset_id>`
![image](https://i.imgur.com/ZGcu04f.gif)

## Usage
```
$ cp .env-example .env
$ vim .env
```
Edit ```.env``` file with your credentials

```
// Updating your dataset
$ python update.py <your_dataset_id>
// Checking Lumen Library
$ python library.py
```

Other alternative methods such as webhooks or Kubernates settings will be provided soon ...
