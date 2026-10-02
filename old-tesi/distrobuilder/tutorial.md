Creare e costruire l'immagine:
```bash
sudo distrobuilder build-incus ubuntu.yaml
```

in output ottengo
* `incus.tar.xz`
* `rootfs.squashfs`

aggiungere l'immagine ad incus:
```bash
incus image import incus.tar.xz rootfs.squashfs --alias container
```


eseguire l'immagine:
```bash
incus launch container c1
```


## generators
