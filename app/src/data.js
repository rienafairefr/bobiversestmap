
export function url_for(t) {
    if (process.env.VUE_APP_DATA_ROOT) {
        return `${process.env.VUE_APP_DATA_ROOT}/${t}`;
    } else {
        return `data/${t}`;
    }
}