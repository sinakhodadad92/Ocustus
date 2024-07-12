export interface JobDetails {
  id: number;
  panels: Panel[];
  job_state: string;
  name: string;
  config: string;
  position: string;
}

export interface Panel {
  errors: Error[];
  panel_photo: string;
  cropped_panel_photo: string;
  id: number;
  panel_number: number | null;
}

export interface Error {
  id: number;
  designator: string;
  rework: boolean;
  coordinate_x: number;
  coordinate_y: number;
  component_image: string;
  component_value: string;
  board_id: number;
  panel_id: number;
}
