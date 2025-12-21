// src/app/admin/leave-requests/page.tsx
'use client';
import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import AdminLayout from '@/components/AdminLayout';
import { db } from '@/lib/db';
import { LeaveRequest } from '@/types';

export default function LeaveRequestsPage() {
  const [leaveRequests, setLeaveRequests] = useState<LeaveRequest[]>([]);

  useEffect(() => {
    loadLeaveRequests();
  }, []);

  const loadLeaveRequests = () => {
    setLeaveRequests(db.getLeaveRequests());
  };

  const handleApproval = (id: string, status: 'approved' | 'rejected', isPaid: boolean = false) => {
    const requests = db.getLeaveRequests();
    const request = requests.find(req => req.id === id);
    
    if (request) {
      const updatedRequest = { ...request, status, isPaid };
      db.updateLeaveRequest(id, updatedRequest);
      loadLeaveRequests();
    }
  };

  const exportLeaveSummary = () => {
    const csvContent = [
      ['Employee', 'Leave Type', 'Start Date', 'End Date', 'Days', 'Status', 'Paid', 'Reason'],
      ...leaveRequests.map(request => {
        const startDate = new Date(request.startDate);
        const endDate = new Date(request.endDate);
        const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
        
        return [
          request.employeeName,
          request.leaveType,
          request.startDate,
          request.endDate,
          days.toString(),
          request.status,
          request.isPaid ? 'Yes' : 'No',
          request.reason
        ];
      })
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'leave_summary.csv';
    a.click();
  };

  const pendingRequests = leaveRequests.filter(req => req.status === 'pending');
  const processedRequests = leaveRequests.filter(req => req.status !== 'pending');

  return (
    <ProtectedRoute adminOnly>
      <AdminLayout>
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
            {/* Header */}
            <div className="flex justify-between items-center">
              <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-amber-500 to-yellow-600">
                Leave Request Management
              </h2>
              <button
                onClick={exportLeaveSummary}
                className="group bg-gradient-to-r from-yellow-400 via-amber-500 to-yellow-600 hover:from-yellow-300 hover:via-amber-400 hover:to-yellow-500 text-black font-bold px-6 py-3 rounded-xl shadow-2xl hover:shadow-yellow-400/25 transition-all duration-300 ease-in-out transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <span className="relative z-10 flex items-center gap-2">
                  📊 Export Leave Summary
                </span>
              </button>
            </div>

            {/* Pending Requests */}
            <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
              {/* Premium Border Glow */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
              
              <div className="relative z-10">
                <div className="px-6 py-5 bg-gradient-to-r from-yellow-400/10 to-amber-500/10 border-b border-yellow-400/20">
                  <h3 className="text-xl font-bold text-yellow-400 flex items-center gap-3">
                    <span className="text-2xl">⏳</span>
                    Pending Requests ({pendingRequests.length})
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-yellow-400/20">
                    <thead className="bg-gradient-to-r from-gray-800/50 to-gray-900/50">
                      <tr>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Employee</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Leave Type</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Duration</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Reason</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Applied Date</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-yellow-400/10">
                      {pendingRequests.map((request) => {
                        const startDate = new Date(request.startDate);
                        const endDate = new Date(request.endDate);
                        const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
                        
                        return (
                          <tr key={request.id} className="hover:bg-yellow-400/5 transition-colors duration-200">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-white">
                              {request.employeeName}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.leaveType}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.startDate} to {request.endDate} ({days} days)
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-300 max-w-xs truncate">
                              {request.reason}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.appliedDate}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                              <button
                                onClick={() => handleApproval(request.id, 'approved', true)}
                                className="group bg-gradient-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 text-white px-3 py-2 rounded-lg text-xs font-semibold shadow-lg hover:shadow-green-500/25 transition-all duration-300 transform hover:scale-105 relative overflow-hidden"
                              >
                                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                                <span className="relative z-10">✅ Approve (Paid)</span>
                              </button>
                              <button
                                onClick={() => handleApproval(request.id, 'approved', false)}
                                className="group bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white px-3 py-2 rounded-lg text-xs font-semibold shadow-lg hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-105 relative overflow-hidden"
                              >
                                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                                <span className="relative z-10">📋 Approve (Unpaid)</span>
                              </button>
                              <button
                                onClick={() => handleApproval(request.id, 'rejected')}
                                className="group bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white px-3 py-2 rounded-lg text-xs font-semibold shadow-lg hover:shadow-red-500/25 transition-all duration-300 transform hover:scale-105 relative overflow-hidden"
                              >
                                <div className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                                <span className="relative z-10">❌ Reject</span>
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Processed Requests */}
            <div className="bg-gradient-to-br from-gray-900/95 via-black/98 to-gray-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-yellow-400/20 overflow-hidden relative">
              {/* Premium Border Glow */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-yellow-400/20 via-amber-500/20 to-yellow-400/20 blur-xl opacity-60" />
              
              <div className="relative z-10">
                <div className="px-6 py-5 bg-gradient-to-r from-gray-800/30 to-gray-900/30 border-b border-yellow-400/20">
                  <h3 className="text-xl font-bold text-gray-300 flex items-center gap-3">
                    <span className="text-2xl">📋</span>
                    Processed Requests ({processedRequests.length})
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-yellow-400/20">
                    <thead className="bg-gradient-to-r from-gray-800/50 to-gray-900/50">
                      <tr>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Employee</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Leave Type</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Duration</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-4 text-left text-xs font-bold text-yellow-400 uppercase tracking-wider">Paid</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-yellow-400/10">
                      {processedRequests.map((request) => {
                        const startDate = new Date(request.startDate);
                        const endDate = new Date(request.endDate);
                        const days = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
                        
                        return (
                          <tr key={request.id} className="hover:bg-yellow-400/5 transition-colors duration-200">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-white">
                              {request.employeeName}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.leaveType}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.startDate} to {request.endDate} ({days} days)
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold shadow-lg ${
                                request.status === 'approved' 
                                  ? 'bg-gradient-to-r from-green-600 to-green-700 text-white' 
                                  : 'bg-gradient-to-r from-red-600 to-red-700 text-white'
                              }`}>
                                {request.status === 'approved' ? '✅' : '❌'} {request.status.toUpperCase()}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {request.status === 'approved' ? (
                                <span className={`inline-flex items-center px-2 py-1 rounded-lg text-xs font-semibold ${
                                  request.isPaid 
                                    ? 'bg-yellow-400/20 text-yellow-400 border border-yellow-400/30' 
                                    : 'bg-gray-600/20 text-gray-400 border border-gray-600/30'
                                }`}>
                                  {request.isPaid ? '💰 Yes' : '📋 No'}
                                </span>
                              ) : (
                                <span className="text-gray-500">-</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </AdminLayout>
    </ProtectedRoute>
  );
}