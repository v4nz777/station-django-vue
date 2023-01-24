export const toTitleCase = (str:string)=> {
    let result:string;
    if(str.length <= 3) result = str.toUpperCase()
    else result = str[0].toUpperCase()+str.slice(1)
    return result
}