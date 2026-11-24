# Resolves the secret number from a directory listing without parsing ls output.
count_directory_entries() {
  local directory=$1
  [[ -d $directory && -r $directory && -x $directory ]] || return 1
  (
    shopt -s nullglob
    shopt -u dotglob failglob
    unset GLOBIGNORE
    entries=("$directory"/*)
    printf '%d\n' "${#entries[@]}"
  )
}
