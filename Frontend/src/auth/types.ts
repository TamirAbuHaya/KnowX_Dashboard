export type UserRole = "BC" | "PC" | "TC" | "CAD" | "ADMIN" | string;

export interface MeResponse {
  id?: number | string;
  email: string;
  full_name?: string;
  role?: UserRole;

  // Your backend fields (may or may not all be returned by /me)
  rank?: string;
  course_num?: number;
  battalion?: string;
  platoon?: number | null;
  team?: number | null;

  must_change_password: boolean;

  // Django flags (often present)
  is_staff?: boolean;
  is_superuser?: boolean;
}
