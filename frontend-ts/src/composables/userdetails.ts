import axios from "axios";
import moment from "moment";

export interface Position {
  id:any|null;
  title: string;
  salary_1?: number;
  salary_2?: number;
  salary_3?: number;
  salary_4?: number;
  salary_5?: number;
}

export const getPosition = async (id: number | null) => {
  if (id) {
    const response = await axios.get(`position/${id}`);
    if (response.status === 200) {
      return response.data as Position;
    } else return { title: "unassigned" } as Position;
  } else return { title: "unassigned" } as Position;
};
export const getPositions = async (filter: string) => {
  const response = await axios.get(`positions/${filter}`);
  const data: Array<Position> = response.data;
  return data;
};

export const useActivityStatus = (
  is_logged: boolean,
  last_active: string | null | undefined
) => {
  if (is_logged) return "Active now";
  else {
    const out = moment(last_active).fromNow();
    return `Active ${out}`;
  }
};
