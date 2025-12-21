// src/app/employee/page.tsx
'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import EmployeeLayout from '@/components/EmployeeLayout';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { formatTime, formatDate, isLateLogin } from '@/lib/utils';
import { AttendanceRecord, Employee, LeaveRequest } from '@/types';

export default function EmployeeDashboard() {
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [todayAttendance, setTodayAttendance] = useState<AttendanceRecord | null>(null);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [recentLeaves, setRecentLeaves] = useState<LeaveRequest[]>([]);
  const [weeklyAttendance, setWeeklyAttendance] = useState<AttendanceRecord[]>([]);
  const router = useRouter();

  useEffect(() => {
    const user = auth.getCurrentUser();
    if (user) {
      loadEmployeeData(user.id);
      loadTodayAttendance(user.id);
      loadRecentLeaves(user.id);
      loadWeeklyAttendance(user.id);
    }

    // Update current time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const loadEmployeeData = (employeeId: string) => {
    const employees = db.getEmployees();
    const emp = employees.find(e => e.id === employeeId);
    setEmployee(emp || null);
  };

  const loadTodayAttendance = (employeeId: string) => {
    const today = formatDate(new Date());
    const attendance = db.getAttendanceRecords();
    const todayRecord = attendance.find(
      record => record.employeeId === employeeId && record.date === today
    );
    setTodayAttendance(todayRecord || null);
    setIsLoggedIn(!!todayRecord && !todayRecord.logoutTime);
  };

  const loadRecentLeaves = (employeeId: string) => {
    const leaves = db.getLeaveRequests();
    const employeeLeaves = leaves
      .filter(leave => leave.employeeId === employeeId)
      .sort((a, b) => new Date(b.appliedDate).getTime() - new Date(a.appliedDate).getTime())
      .slice(0, 3);
    setRecentLeaves(employeeLeaves);
  };

  const loadWeeklyAttendance = (employeeId: string) => {
    const attendance = db.getAttendanceRecords();
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    
    const weeklyRecords = attendance.filter(record => 
      record.employeeId === employeeId && 
      new Date(record.date) >= oneWeekAgo
    ).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    
    setWeeklyAttendance(weeklyRecords);
  };

  const handleCheckIn = () => {
    if (!employee) return;

    const now = new Date();
    const loginTime = formatTime(now);
    const isLate = isLateLogin(loginTime);

    const attendanceRecord: AttendanceRecord = {
      id: Date.now().toString(),
      employeeId: employee.id,
      employeeName: employee.name,
      date: formatDate(now),
      loginTime,
      isLate,
      location: 'Office' // You can enhance this to get actual location
    };

    db.addAttendanceRecord(attendanceRecord);
    setTodayAttendance(attendanceRecord);
    setIsLoggedIn(true);
  };

  const handleCheckOut = () => {
    if (!todayAttendance) return;

    const now = new Date();
    const logoutTime = formatTime(now);
    const totalHours = calculateWorkingHours(todayAttendance.loginTime, logoutTime);

    const updatedRecord = {
      ...todayAttendance,
      logoutTime,
      totalHours
    };

    db.updateAttendanceRecord(todayAttendance.id, updatedRecord);
    setTodayAttendance(updatedRecord);
    setIsLoggedIn(false);
  };

  const calculateWorkingHours = (loginTime: string, logoutTime: string): number => {
    const login = new Date(`2000-01-01 ${loginTime}`);
    const logout = new Date(`2000-01-01 ${logoutTime}`);
    const diff = logout.getTime() - login.getTime();
    return Math.round((diff / (1000 * 60 * 60)) * 100) / 100;
  };

  if (!employee) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-black flex items-center justify-center">
          <div className="text-xl text-yellow-400 font-bold">Loading...</div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <EmployeeLayout>
        <div className="min-h-screen bg-black relative overflow-hidden">
          {/* Animated Background Elements */}
          <div className="absolute inset-0">
            <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-yellow-400/10 to-amber-500/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-20 right-10 w-96 h-96 bg-gradient-to-l from-yellow-300/8 to-yellow-600/8 rounded-full blur-3xl animate-pulse delay-1000" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-tr from-amber-400/5 to-yellow-500/5 rounded-full blur-3xl animate-pulse delay-500" />
          </div>

          {/* Golden Grid Pattern Overlay */}
          <div className="absolute inset-0 opacity-5" style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, rgb(255, 215, 0) 1px, transparent 0)`,
            backgroundSize: '40px 40px'
          }} />

          <div className="relative z-10 p-6 space-y-6">
            {/* Welcome Section */}
            <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative p-8">
              {/* Premium Border Glow */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
              
              <div className="relative z-10 flex justify-between items-center">
                <div>
                  <h2 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-amber-500 to-yellow-600 mb-3">
                    Good {currentTime.getHours() < 12 ? 'Morning' : currentTime.getHours() < 17 ? 'Afternoon' : 'Evening'}, {employee.name}!
                  </h2>
                  <p className="text-yellow-300/80 text-lg font-semibold">
                    {employee.position} • {employee.department}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-mono text-yellow-400 font-bold">
                    {currentTime.toLocaleTimeString()}
                  </div>
                  <div className="text-yellow-300/70 font-medium">
                    {currentTime.toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Check In/Out Card */}
              <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
                
                <div className="relative z-10 p-6">
                  <h3 className="text-xl font-bold text-yellow-400 mb-6 flex items-center gap-2">
                    <span className="text-2xl">🕒</span>
                    Today&apos;s Attendance
                  </h3>
                  
                  {todayAttendance ? (
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                        <span className="text-gray-300">Check In:</span>
                        <span className={`font-bold ${todayAttendance.isLate ? 'text-red-400' : 'text-green-400'}`}>
                          {todayAttendance.loginTime} {todayAttendance.isLate && '(Late)'}
                        </span>
                      </div>
                      
                      {todayAttendance.logoutTime && (
                        <>
                          <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                            <span className="text-gray-300">Check Out:</span>
                            <span className="font-bold text-blue-400">
                              {todayAttendance.logoutTime}
                            </span>
                          </div>
                          <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                            <span className="text-gray-300">Total Hours:</span>
                            <span className="font-bold text-purple-400">
                              {todayAttendance.totalHours}h
                            </span>
                          </div>
                        </>
                      )}
                      
                      {isLoggedIn ? (
                        <button
                          onClick={handleCheckOut}
                          className="group w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white font-bold py-3 px-4 rounded-xl shadow-2xl hover:shadow-red-500/25 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden"
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                          <span className="relative z-10">🚪 Check Out</span>
                        </button>
                      ) : todayAttendance.logoutTime ? (
                        <div className="w-full bg-gradient-to-r from-gray-600/50 to-gray-700/50 text-gray-300 font-bold py-3 px-4 rounded-xl text-center border border-gray-600/30">
                          ✅ Day Completed
                        </div>
                      ) : null}
                    </div>
                  ) : (
                    <div className="text-center">
                      <p className="text-gray-400 mb-6 text-lg">You haven&apos;t checked in today</p>
                      <button
                        onClick={handleCheckIn}
                        className="group w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 text-white font-bold py-3 px-4 rounded-xl shadow-2xl hover:shadow-green-500/25 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden"
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                        <span className="relative z-10">🚀 Check In</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
                
                <div className="relative z-10 p-6">
                  <h3 className="text-xl font-bold text-yellow-400 mb-6 flex items-center gap-2">
                    <span className="text-2xl">⚡</span>
                    Quick Actions
                  </h3>
                  <div className="space-y-4">
                    <button
                      onClick={() => router.push('/employee/attendance')}
                      className="group w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white font-bold py-3 px-4 rounded-xl shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      <span className="relative z-10 flex items-center justify-center gap-2">
                        <span>🕒</span>
                        View Attendance
                      </span>
                    </button>
                    <button
                      onClick={() => router.push('/employee/leave')}
                      className="group w-full bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-500 hover:to-yellow-600 text-white font-bold py-3 px-4 rounded-xl shadow-2xl hover:shadow-yellow-500/25 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      <span className="relative z-10 flex items-center justify-center gap-2">
                        <span>📝</span>
                        Request Leave
                      </span>
                    </button>
                  </div>
                </div>
              </div>

              {/* Stats Card */}
              <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
                
                <div className="relative z-10 p-6">
                  <h3 className="text-xl font-bold text-yellow-400 mb-6 flex items-center gap-2">
                    <span className="text-2xl">📊</span>
                    This Week&apos;s Stats
                  </h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                      <span className="text-gray-300">Days Present:</span>
                      <span className="font-bold text-green-400 text-lg">
                        {weeklyAttendance.length}
                      </span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                      <span className="text-gray-300">Late Arrivals:</span>
                      <span className="font-bold text-red-400 text-lg">
                        {weeklyAttendance.filter(record => record.isLate).length}
                      </span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-800/30 rounded-xl border border-yellow-400/10">
                      <span className="text-gray-300">Total Hours:</span>
                      <span className="font-bold text-blue-400 text-lg">
                        {weeklyAttendance.reduce((sum, record) => sum + (record.totalHours || 0), 0)}h
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Recent Attendance */}
              <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
                
                <div className="relative z-10">
                  <div className="px-6 py-5 bg-gradient-to-r from-yellow-400/10 to-amber-500/10 border-b border-yellow-400/20">
                    <h3 className="text-xl font-bold text-yellow-400 flex items-center gap-3">
                      <span className="text-2xl">📅</span>
                      Recent Attendance
                    </h3>
                  </div>
                  <div className="p-6 space-y-3">
                    {weeklyAttendance.slice(0, 5).map((record) => (
                      <div key={record.id} className="flex justify-between items-center p-4 bg-gray-800/30 rounded-xl border border-yellow-400/10 hover:bg-yellow-400/5 transition-colors duration-200">
                        <div>
                          <div className="font-bold text-white text-lg">
                            {new Date(record.date).toLocaleDateString('en-US', {
                              weekday: 'short',
                              month: 'short',
                              day: 'numeric'
                            })}
                          </div>
                          <div className="text-sm text-gray-400">
                            {record.loginTime} - {record.logoutTime || 'Active'}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-sm font-bold mb-1 ${record.isLate ? 'text-red-400' : 'text-green-400'}`}>
                            {record.isLate ? '🔴 Late' : '🟢 On Time'}
                          </div>
                          <div className="text-sm text-gray-400 font-semibold">
                            {record.totalHours ? `${record.totalHours}h` : '0h'}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Recent Leave Requests */}
              <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
                <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
                
                <div className="relative z-10">
                  <div className="px-6 py-5 bg-gradient-to-r from-yellow-400/10 to-amber-500/10 border-b border-yellow-400/20">
                    <h3 className="text-xl font-bold text-yellow-400 flex items-center gap-3">
                      <span className="text-2xl">📋</span>
                      Recent Leave Requests
                    </h3>
                  </div>
                  <div className="p-6 space-y-3">
                    {recentLeaves.length === 0 ? (
                      <p className="text-gray-400 text-center py-8 text-lg">No leave requests yet</p>
                    ) : (
                      recentLeaves.map((leave) => (
                        <div key={leave.id} className="p-4 bg-gray-800/30 rounded-xl border border-yellow-400/10 hover:bg-yellow-400/5 transition-colors duration-200">
                          <div className="flex justify-between items-start mb-3">
                            <div className="font-bold text-white text-lg">
                              {leave.leaveType}
                            </div>
                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold shadow-lg ${
                              leave.status === 'approved' 
                                ? 'bg-gradient-to-r from-green-600 to-green-700 text-white'
                                : leave.status === 'rejected'
                                ? 'bg-gradient-to-r from-red-600 to-red-700 text-white'
                                : 'bg-gradient-to-r from-yellow-600 to-yellow-700 text-white'
                            }`}>
                              {leave.status === 'approved' ? '✅' : leave.status === 'rejected' ? '❌' : '⏳'} {leave.status.toUpperCase()}
                            </span>
                          </div>
                          <div className="text-sm text-gray-400 mb-2">
                            {leave.startDate} to {leave.endDate}
                          </div>
                          {leave.status === 'approved' && (
                            <div className="text-xs font-semibold">
                              <span className={`inline-flex items-center px-2 py-1 rounded-lg ${
                                leave.isPaid 
                                  ? 'bg-yellow-400/20 text-yellow-400 border border-yellow-400/30' 
                                  : 'bg-gray-600/20 text-gray-400 border border-gray-600/30'
                              }`}>
                                {leave.isPaid ? '💰 Paid Leave' : '📋 Unpaid Leave'}
                              </span>
                            </div>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </EmployeeLayout>
    </ProtectedRoute>
  );
}