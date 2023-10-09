import moment from "moment";

/** Reformat timestamp, to be more human readable */
export const timeStamp = (date: string) =>{
    const humanized = moment(date).fromNow();
    return humanized;
}

