## [v0.3.4](git@github.com:pruizlezcano/comicgeeks/compare/v0.3.3...v0.3.4) (2023-12-08)

### Bug Fixes

- **Issue**: Fixed missing image attribute in variant covers [[#4](https://github.com/pruizlezcano/comicgeeks/issues/4)] ([793f0b5](git@github.com:pruizlezcano/comicgeeks/commit/793f0b5a116a7047f8c3319c03e7842d2cbc0342))

## [v0.3.3](https://github.com/pruizlezcano/comicgeeks/compare/v0.3.2...v0.3.3) (2023-11-30)

### Bug Fixes

- **Issue**: Fixed new location for price and page values [[#3](https://github.com/pruizlezcano/comicgeeks/issues/3)] ([6203375](https://github.com/pruizlezcano/comicgeeks/commit/62033753d8796ce451632b9704434839b7b6b4ab))

## 0.3.2 (2023-09-01)

### Fixes

- **Issue:** error when series doesn't have any trade paperback ([8bbd122](https://github.com/pruizlezcano/comicgeeks/commit/8bbd1223a5b803e4a3dfbac013e1fdaf8bbdc1a9))

## 0.3.1 (2023-08-31)

### Fixes

- url error when getting data ([39b9d62](https://github.com/pruizlezcano/comicgeeks/commit/39b9d629a66c49dc1b8ffdef8ef805e7f855c231))
- error getting trade paperback name ([1c37d74](https://github.com/pruizlezcano/comicgeeks/commit/1c37d74da6179e19c7a387e79867bc872dd05f82))

### Tests

- compare timestamps from different timezones ([4009fd1](https://github.com/pruizlezcano/comicgeeks/commit/4009fd189aa1e4807344b3f4d5065d430d46b589))
- pass test variables ([84a9db4](https://github.com/pruizlezcano/comicgeeks/commit/84a9db4b2607f0a52dbb35d7b35502fadfde120d))

## 0.3.0 (2023-07-11)

### Features

- login with user and password ([422d044](https://github.com/pruizlezcano/comicgeeks/commit/422d04426e198f9c691c0443cb0f1d48f7a54602))
- added TradePaperback class ([3620470](https://github.com/pruizlezcano/comicgeeks/commit/3620470d4e3f1a0bd12193f3bdb038e37261f02c))
- added github actions ([46f4639](https://github.com/pruizlezcano/comicgeeks/commit/46f46396df44ad949f51bab1731bea67bba01705))

### Fixes

- new issue name location ([f837c74](https://github.com/pruizlezcano/comicgeeks/commit/f837c74eb03096d1e3ddc4adf92571543f685862))
- module export ([9981d02](https://github.com/pruizlezcano/comicgeeks/commit/9981d02557704b124c3e9e580e97a22a46691139))

### Tests

- update for the new session system ([17bacc7](https://github.com/pruizlezcano/comicgeeks/commit/17bacc74000bb1e1a095138f773202b4af4bcd1c))
- fixed github actions secrets ([2f8ce3c](https://github.com/pruizlezcano/comicgeeks/commit/2f8ce3c54926bb78ccde8eef4bd23693098d9e6c), [8b95823](https://github.com/pruizlezcano/comicgeeks/commit/8b95823705eb42db82268f6c6d48d53318fe4bf6), [8db643d](https://github.com/pruizlezcano/comicgeeks/commit/8db643d334237aab4d1a58e49713a2b6e2aa73e5))

### Refactors

- share client session for all classes ([c6c174b](https://github.com/pruizlezcano/comicgeeks/commit/c6c174bf8a9ca32b82d45e9057a279aa85b9b650))

### Documentation

- added login method and Trade_Paperback class ([40c4094]())

## 0.2.3 (2023-04-08)

### Fixes

- **issue:** error getting rating of new issues that haven't had any ratings [#2](https://github.com/pruizlezcano/comicgeeks/issues/2) ([b402714](https://github.com/pruizlezcano/comicgeeks/commit/b40271400e877e792b1be9a2a458e6f5a9eb2eba))

## 0.2.2 (2023-01-16)

### Fixes

- **deps:** install necessary dependencies [#1](https://github.com/pruizlezcano/comicgeeks/issues/1) ([52f832d](https://github.com/pruizlezcano/comicgeeks/commit/52f832dd9f36ddf167e0efd916c44320c80444ba))

## 0.2.1 (2022-09-12)

### Fixes

- **issue:** error when some data is not available ([122df9b](https://github.com/pruizlezcano/comicgeeks/commit/122df9b23b5b8e34243dc20ed106b39c08d618f7))

## 0.2.0 (2022-08-08)

### Features

- **test:** added tests ([2323816](https://github.com/pruizlezcano/comicgeeks/commit/23238164e778de6e786f127974a6fe7db2d18ec5))
- **new_releases:** get releases from input date ([9ddcee1](https://github.com/pruizlezcano/comicgeeks/commit/9ddcee195154b9fbb9c8be4e787e26ba4c814318))
- search character by name ([55ff1c1](https://github.com/pruizlezcano/comicgeeks/commit/55ff1c17c5a93463988eaf1d949a410e89fc2f7e))
- search creator by name ([7353372](https://github.com/pruizlezcano/comicgeeks/commit/735337234ec9c8a865f4970cd0d68d9344438d9f))

### Refactors

- **session:** use only one session for each class ([8baa9f1](https://github.com/pruizlezcano/comicgeeks/commit/8baa9f1f8c71a46351226ce81c796bf5cb634308))

### Documentation Changes

- update docs ([8b59f6d](https://github.com/pruizlezcano/comicgeeks/commit/8b59f6d5989b160146564247aa6cbfc4410d9bf2))

## 0.1.0 (2022-08-01)

### Features

- Initial commit ([83277e0](https://github.com/pruizlezcano/comicgeeks/commit/83277e07bd17b4bd68684302cf6908759300f142))
- First release ([4ef2898](https://github.com/pruizlezcano/comicgeeks/commit/4ef28988ec751ad58187174eeb948539c3bfc6f6))

### Fixes

- **docs** Error building docs ([eb03282](https://github.com/pruizlezcano/comicgeeks/commit/eb03282f15c5684720fed27626cbff23f818455c))
- **docs** More build errors ([fe3f7b1](https://github.com/pruizlezcano/comicgeeks/commit/fe3f7b146c8ba5d098a8ed583511e6c833d55a01))
- **docs** More build errors -\_- ([e227707](https://github.com/pruizlezcano/comicgeeks/commit/e2277079e7e0d56ef4963788dc42d0f176a85671))
