import moment from "moment";

/** Reformat timestamp, to be more human readable */
export const timeStamp = (date: string) =>{
    const humanized = moment(date).subtract(8, "hours").fromNow();
    return humanized;
}

