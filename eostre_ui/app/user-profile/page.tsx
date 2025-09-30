"use client";

import { useState } from "react";
import { Button } from "@ui-components/Button";
import { ProtectedRoute } from "@utils/ProtectedRoute";
import { useUser } from "@utils/userProvider";
import ProfileEditDrawer from "./ProfileEditDrawer";
import { AddEmailDrawer } from "@ui-components/AddEmailDrawer";


export default function ProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileContent />
    </ProtectedRoute>
  );
}

function ProfileContent() {
  const { userProfile, loading, error } = useUser();
  const [isEditOpen, setEditOpen] = useState(false);
  const [isAddEmailOpen, setAddEmailOpen] = useState(false);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!userProfile) return <p>No profile data</p>;

  return (
    <>
      <div className="font-sans min-h-screen p-8 sm:p-20 bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light">
        <main className="flex flex-col gap-8 w-full">
          <div className="w-full flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold text-brand-primary dark:text-accent-cyan">
              {userProfile.display_name}
            </h1>
            <Button
              onClick={() => setEditOpen(true)}
              aria-label="Open Edit User Drawer"
            >
              Edit
            </Button>
          </div>
          <section>
            <h2 className="text-lg font-semibold mb-2">Profile Information</h2>
            <ul className="space-y-1">
              <li><span className="font-medium">Username:</span> {userProfile.name}</li>
              {userProfile.personal_name && (
                <li><span className="font-medium">Personal Name:</span> {userProfile.personal_name}</li>
              )}
              {userProfile.family_names && (
                <li><span className="font-medium">Family Names:</span> {userProfile.family_names}</li>
              )}
              <li><span className="font-medium">Type:</span> {userProfile.type}</li>
              <li><span className="font-medium">Created:</span> {new Date(userProfile.created_date).toLocaleString()}</li>
            </ul>
          </section>

          {/* Emails table */}
          <section>
            <div className="w-full flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold mb-2">Emails</h2>
              <Button
                onClick={() => setAddEmailOpen(true)}
                size="sm"
                aria-label="Open Add Email Drawer"
              >
                + Add
              </Button>
            </div>
            <AddEmailDrawer
              isOpen={isAddEmailOpen}
              onClose={() => setAddEmailOpen(false)}
            />
            <div className="overflow-x-auto">
              <table className="min-w-full border border-brand-dark dark:border-brand-light rounded-lg">
                <thead className="bg-brand-dark text-brand-light dark:bg-brand-light dark:text-brand-dark">
                  <tr>
                    <th className="px-4 py-2 text-left">Email</th>
                    <th className="px-4 py-2 text-left">Primary</th>
                    <th className="px-4 py-2 text-left">Validated</th>
                    <th className="px-4 py-2 text-left">Created</th>
                    <th className="px-4 py-2 text-left">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {userProfile.emails.map((email: any) => (
                    <tr
                      key={email.id}
                      className="border-t border-brand-dark dark:border-brand-light"
                    >
                      <td className="px-4 py-2">{email.email}</td>
                      <td className="px-4 py-2">
                        {email.primary ? (
                          <span className="text-green-600 font-medium">✔</span>
                        ) : (
                          ""
                        )}
                      </td>
                      <td className="px-4 py-2">
                        {email.validated ? (
                          <span className="text-green-600 font-medium">✔</span>
                        ) : (
                          <span className="text-red-500 font-medium">✘</span>
                        )}
                      </td>
                      <td className="px-4 py-2">
                        {new Date(email.created_date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-2">
                        {!email.primary && (
                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => console.log("TODO: setPrimary", email.id)}
                          >
                            Make Primary
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
        {isEditOpen && (
          <ProfileEditDrawer
            userProfile={userProfile}
            onClose={() => setEditOpen(false)}
          />
        )}
      </div>
    </>
  );
}
