import React from "react";

export const api_url = "http://127.0.0.1:5092/";
// Define TypeScript interfaces
export interface AppData {
  name: string;
  display_id: string;
  launch_count: number;
}
export interface AppComponent {
  name: string;
  display_id: string;
  launch_count: number;
  setGlobalId:React.Dispatch<React.SetStateAction<string>>;
  setGlobalAppName:React.Dispatch<React.SetStateAction<string>>;
}
export interface AppsResponse {
  favourites: AppData[];
  app_list: AppData[];
}
