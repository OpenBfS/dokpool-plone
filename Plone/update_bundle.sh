rm -Rf src/docpool.theme/docpool/theme/webpack_resources/theme/docpooltheme/
mkdir src/docpool.theme/docpool/theme/webpack_resources/theme/docpooltheme/
cd src/docpool.theme/docpool/theme/webpack_resources/
npm run build
cd -
git add src/docpool.theme/docpool/theme/webpack_resources/theme/docpooltheme/
git commit -m "Update bundle files" src/docpool.theme/docpool/theme/webpack_resources/theme/docpooltheme/
