// src/types/index.ts
export interface Employee {
  id: string;
  name: string;
  email: string;
  username: string;
  password: string;
  department: string;
  position: string;
  salary: number;
  joinDate: string;
}

export interface AttendanceRecord {
  id: string;
  employeeId: string;
  employeeName: string;
  date: string;
  loginTime: string;
  logoutTime?: string;
  totalHours?: number;
  isLate: boolean;
  location: string;
}

export interface LeaveRequest {
  id: string;
  employeeId: string;
  employeeName: string;
  leaveType: string;
  startDate: string;
  endDate: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  isPaid: boolean;
  appliedDate: string;
}

export interface PayrollRecord {
  id: string;
  employeeId: string;
  employeeName: string;
  baseSalary: number;
  workingDays: number;
  paidLeaves: number;
  unpaidLeaves: number;
  deductions: number;
  finalSalary: number;
  month: string;
  year: number;
}