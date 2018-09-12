# acts-saflii

This is a script to archive the documents on [indigo.africanlii.org] into a
structure that can be ingested into [SAFLII](http://www.saflii.org/) by pulling them from the Indigo server at [indigo.africanlii.org](https://indigo.africanlii.org).

## Using this script

1. Clone it from GitHub:

    ```bash
    git clone https://github.com/Code4SA/openbylaws-saflii.git
    cd openbylaws-saflii
    ```

2. Install dependencies using [pip](https://pip.pypa.io/en/stable/):

    ```bash
    pip install -r requirements.txt
    ```

3. To install the crontab that updates the by-laws every morning, use ``crontab crontab``. THIS WILL OVERRIGHT YOUR EXISTING CRONTAB!

4. Run the archiver, giving it a target directory where to put the documents:

    ```bash
    python archive.py --target /tmp/bylaws-test -regions za-cpt
    ```


## Updating this script

When there's a new version, just use ``git pull`` to update:

```bash
cd saflii-legislation
git pull
```

# License

Licensed under the MIT License.
