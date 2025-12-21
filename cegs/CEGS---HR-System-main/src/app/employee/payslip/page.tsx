// src/app/employee/payslip/page.tsx
'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import EmployeeLayout from '@/components/EmployeeLayout';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { PayslipGenerator, formatCurrency, getAvailableMonths } from '@/lib/payslip';
import { PayslipData, Employee, SalaryStructure } from '@/types';

export default function PayslipPage() {
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [payslips, setPayslips] = useState<PayslipData[]>([]);
  const [salaryStructure, setSalaryStructure] = useState<SalaryStructure | null>(null);
  const [loading, setLoading] = useState(true);
  const [generateLoading, setGenerateLoading] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const user = auth.getCurrentUser();
    if (user) {
      loadEmployeeData(user.id);
      loadPayslips(user.id);
      loadSalaryStructure(user.id);
    }
    setLoading(false);
  }, []);

  const loadEmployeeData = (employeeId: string) => {
    const employees = db.getEmployees();
    const emp = employees.find(e => e.id === employeeId);
    setEmployee(emp || null);
  };

  const loadPayslips = (employeeId: string) => {
    const employeePayslips = db.getEmployeePayslips(employeeId);
    setPayslips(employeePayslips.sort((a, b) => 
      new Date(`${b.year}-${getMonthNumber(b.month)}-01`).getTime() - 
      new Date(`${a.year}-${getMonthNumber(a.month)}-01`).getTime()
    ));
  };

  const loadSalaryStructure = (employeeId: string) => {
    const structure = db.getEmployeeSalaryStructure(employeeId);
    setSalaryStructure(structure);
  };

  const getMonthNumber = (monthName: string): number => {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months.indexOf(monthName) + 1;
  };

  const handleGeneratePayslip = async (month: string, year: number) => {
    if (!employee) return;

    setGenerateLoading(`${month}_${year}`);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const payslip = PayslipGenerator.generatePayslip(employee.id, month, year);
    if (payslip) {
      db.addPayslip(payslip);
      loadPayslips(employee.id);
    }

    setGenerateLoading(null);
  };

  const handleDownloadPayslip = (payslip: PayslipData) => {
    PayslipGenerator.downloadPayslip(payslip);
  };

  const getPayslipStatus = (month: string, year: number): 'available' | 'missing' | 'pending' => {
    const exists = payslips.find(p => p.month === month && p.year === year);
    const currentDate = new Date();
    const payslipDate = new Date(year, getMonthNumber(month) - 1, 1);
    
    if (exists) return 'available';
    if (payslipDate > currentDate) return 'pending';
    return 'missing';
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <EmployeeLayout>
          <div className="min-h-screen flex items-center justify-center">
            <div className="text-yellow-400 text-xl">Loading payslips...</div>
          </div>
        </EmployeeLayout>
      </ProtectedRoute>
    );
  }

  if (!employee) {
    return (
      <ProtectedRoute>
        <EmployeeLayout>
          <div className="text-center py-12">
            <div className="text-red-400 text-xl">Employee data not found</div>
          </div>
        </EmployeeLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <EmployeeLayout>
        <div className="space-y-6">
          {/* Header Section */}
          <div className="relative bg-gradient-to-br from-gray-900/90 via-black/95 to-gray-900/90 backdrop-blur-lg border border-yellow-400/20 p-8 rounded-2xl shadow-2xl overflow-hidden">
            <div className="absolute inset-0">
              <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-yellow-400/10 to-amber-500/10 rounded-full blur-3xl animate-pulse" />
            </div>
            
            <div className="relative z-10">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-amber-500">
                    💰 Payslip Management
                  </h1>
                  <p className="text-yellow-200/80 text-lg mt-2">
                    Download and view your salary slips
                  </p>
                </div>

                {salaryStructure && (
                  <div className="text-right">
                    <div className="text-yellow-400/60 text-sm uppercase tracking-wider">Current Salary</div>
                    <div className="text-3xl font-bold text-yellow-400">
                      {formatCurrency(salaryStructure.basicSalary + 
                        Object.values(salaryStructure.allowances).reduce((sum, val) => sum + val, 0))}
                    </div>
                    <div className="text-yellow-200/60 text-sm">per month</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-green-500/20 p-4 rounded-xl">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">{payslips.length}</div>
                <div className="text-gray-300 text-sm">Available Payslips</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-blue-500/20 p-4 rounded-xl">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">
                  {payslips.length > 0 ? formatCurrency(payslips[0]?.netSalary || 0) : '₹0'}
                </div>
                <div className="text-gray-300 text-sm">Latest Salary</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-purple-500/20 p-4 rounded-xl">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">
                  {payslips.reduce((sum, p) => sum + p.netSalary, 0) > 0 ? 
                    formatCurrency(payslips.reduce((sum, p) => sum + p.netSalary, 0)) : '₹0'}
                </div>
                <div className="text-gray-300 text-sm">YTD Earnings</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-amber-500/20 p-4 rounded-xl">
              <div className="text-center">
                <div className="text-2xl font-bold text-amber-400">
                  {payslips.reduce((sum, p) => sum + (p.deductions.tax + p.deductions.providentFund + p.deductions.insurance + p.deductions.other), 0) > 0 ?
                    formatCurrency(payslips.reduce((sum, p) => sum + (p.deductions.tax + p.deductions.providentFund + p.deductions.insurance + p.deductions.other), 0)) : '₹0'}
                </div>
                <div className="text-gray-300 text-sm">YTD Deductions</div>
              </div>
            </div>
          </div>

          {/* Payslip List */}
          <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-yellow-400/20 rounded-2xl shadow-2xl overflow-hidden">
            <div className="p-6 border-b border-yellow-400/20">
              <h2 className="text-xl font-bold text-yellow-400 flex items-center">
                <span className="mr-2">📋</span>
                Payslip History
              </h2>
            </div>

            <div className="p-6">
              <div className="space-y-4">
                {getAvailableMonths().map(({ month, year }) => {
                  const existingPayslip = payslips.find(p => p.month === month && p.year === year);
                  const status = getPayslipStatus(month, year);
                  const isGenerating = generateLoading === `${month}_${year}`;

                  return (
                    <div key={`${month}_${year}`} 
                         className="flex items-center justify-between p-4 bg-gray-800/40 rounded-lg border border-yellow-400/10 hover:border-yellow-400/20 transition-all duration-300">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-yellow-400/20 to-amber-500/20 rounded-lg flex items-center justify-center border border-yellow-400/30">
                          <span className="text-yellow-400 font-bold">{month.slice(0, 3)}</span>
                        </div>
                        <div>
                          <div className="font-medium text-yellow-300">{month} {year}</div>
                          <div className="text-sm text-gray-400">
                            {existingPayslip ? 
                              `Net Salary: ${formatCurrency(existingPayslip.netSalary)}` : 
                              'Payslip not generated'}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-3">
                        {status === 'available' && existingPayslip && (
                          <>
                            <button
                              onClick={() => router.push(`/employee/payslip/${month.toLowerCase()}-${year}`)}
                              className="bg-gradient-to-r from-blue-600/20 to-blue-700/20 hover:from-blue-600/30 hover:to-blue-700/30 text-blue-400 border border-blue-500/30 hover:border-blue-400/50 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300"
                            >
                              View Details
                            </button>
                            <button
                              onClick={() => handleDownloadPayslip(existingPayslip)}
                              className="bg-gradient-to-r from-green-600/20 to-green-700/20 hover:from-green-600/30 hover:to-green-700/30 text-green-400 border border-green-500/30 hover:border-green-400/50 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 flex items-center"
                            >
                              <span className="mr-1">📥</span>
                              Download
                            </button>
                          </>
                        )}

                        {status === 'missing' && salaryStructure && (
                          <button
                            onClick={() => handleGeneratePayslip(month, year)}
                            disabled={isGenerating}
                            className="bg-gradient-to-r from-yellow-600/20 to-amber-600/20 hover:from-yellow-600/30 hover:to-amber-600/30 text-yellow-400 border border-yellow-500/30 hover:border-yellow-400/50 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 disabled:opacity-50 flex items-center"
                          >
                            {isGenerating ? (
                              <>
                                <div className="w-4 h-4 border-2 border-yellow-400/30 border-t-yellow-400 rounded-full animate-spin mr-2"></div>
                                Generating...
                              </>
                            ) : (
                              <>
                                <span className="mr-1">⚡</span>
                                Generate
                              </>
                            )}
                          </button>
                        )}

                        {status === 'pending' && (
                          <div className="px-4 py-2 bg-gray-700/50 text-gray-400 rounded-lg text-sm border border-gray-600/30">
                            Future Month
                          </div>
                        )}

                        {status === 'missing' && !salaryStructure && (
                          <div className="px-4 py-2 bg-red-900/30 text-red-400 rounded-lg text-sm border border-red-500/30">
                            No Salary Structure
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              {payslips.length === 0 && salaryStructure && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">💰</div>
                  <div className="text-gray-400 text-lg mb-4">No payslips generated yet</div>
                  <div className="text-gray-500 text-sm">Click "Generate" to create your first payslip</div>
                </div>
              )}

              {!salaryStructure && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">⚠️</div>
                  <div className="text-red-400 text-lg mb-2">Salary Structure Not Set</div>
                  <div className="text-gray-400">Please contact HR to set up your salary structure</div>
                </div>
              )}
            </div>
          </div>

          {/* Salary Structure Overview */}
          {salaryStructure && (
            <div className="bg-gradient-to-br from-gray-900/60 via-black/80 to-gray-900/60 backdrop-blur-sm border border-yellow-400/20 rounded-2xl shadow-2xl overflow-hidden">
              <div className="p-6 border-b border-yellow-400/20">
                <h2 className="text-xl font-bold text-yellow-400 flex items-center">
                  <span className="mr-2">💼</span>
                  Your Salary Structure
                </h2>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Earnings */}
                  <div className="space-y-4">
                    <h3 className="font-semibold text-green-400 text-center border-b border-green-500/20 pb-2">EARNINGS</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Basic Salary:</span>
                        <span className="text-green-400 font-medium">{formatCurrency(salaryStructure.basicSalary)}</span>
                      </div>
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">House Rent:</span>
                        <span className="text-green-400 font-medium">{formatCurrency(salaryStructure.allowances.houseRent)}</span>
                      </div>
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Medical:</span>
                        <span className="text-green-400 font-medium">{formatCurrency(salaryStructure.allowances.medical)}</span>
                      </div>
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Transport:</span>
                        <span className="text-green-400 font-medium">{formatCurrency(salaryStructure.allowances.transport)}</span>
                      </div>
                      {salaryStructure.allowances.other > 0 && (
                        <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                          <span className="text-gray-300">Other:</span>
                          <span className="text-green-400 font-medium">{formatCurrency(salaryStructure.allowances.other)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Deductions */}
                  <div className="space-y-4">
                    <h3 className="font-semibold text-red-400 text-center border-b border-red-500/20 pb-2">DEDUCTIONS</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Income Tax:</span>
                        <span className="text-red-400 font-medium">{salaryStructure.deductions.taxPercentage}%</span>
                      </div>
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Provident Fund:</span>
                        <span className="text-red-400 font-medium">{salaryStructure.deductions.pfPercentage}%</span>
                      </div>
                      <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                        <span className="text-gray-300">Insurance:</span>
                        <span className="text-red-400 font-medium">{formatCurrency(salaryStructure.deductions.insurance)}</span>
                      </div>
                      {salaryStructure.deductions.other > 0 && (
                        <div className="flex justify-between p-2 bg-gray-800/30 rounded">
                          <span className="text-gray-300">Other:</span>
                          <span className="text-red-400 font-medium">{formatCurrency(salaryStructure.deductions.other)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Summary */}
                  <div className="space-y-4">
                    <h3 className="font-semibold text-yellow-400 text-center border-b border-yellow-500/20 pb-2">SUMMARY</h3>
                    <div className="space-y-3">
                      <div className="p-3 bg-green-900/20 border border-green-500/30 rounded-lg">
                        <div className="text-gray-300 text-sm">Gross Salary</div>
                        <div className="text-green-400 font-bold text-lg">
                          {formatCurrency(salaryStructure.basicSalary + 
                            Object.values(salaryStructure.allowances).reduce((sum, val) => sum + val, 0))}
                        </div>
                      </div>
                      
                      <div className="p-3 bg-amber-900/20 border border-amber-500/30 rounded-lg">
                        <div className="text-gray-300 text-sm">Estimated Deductions</div>
                        <div className="text-amber-400 font-bold">
                          ~{formatCurrency(
                            ((salaryStructure.basicSalary + Object.values(salaryStructure.allowances).reduce((sum, val) => sum + val, 0)) * 
                             salaryStructure.deductions.taxPercentage / 100) +
                            (salaryStructure.basicSalary * salaryStructure.deductions.pfPercentage / 100) +
                            salaryStructure.deductions.insurance +
                            salaryStructure.deductions.other
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </EmployeeLayout>
    </ProtectedRoute>
  );
}