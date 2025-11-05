"use client";

import { useAuth } from "@/components/auth/AuthContext";

import CallToAction from "./topbar/CallToAction";
import HamburgerMenu from "./topbar/HamburgerMenu";
import Logo from "./topbar/Logo";
import Navigation from "./topbar/Navigation";
import Profile from "./topbar/Profile";

export default function Topbar() {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Logo />
          <Navigation className="hidden md:flex" listClassName="space-x-2" />
          <div className="hidden items-center justify-center space-x-2 md:flex">
            <Profile user={user} />
            <CallToAction />
          </div>
          <div className="md:hidden">
            <HamburgerMenu>
              <div className="mt-8 flex flex-col space-y-4">
                <Navigation
                  listClassName="flex flex-col space-y-2 mx-4"
                  orientation="vertical"
                />
                <div className="mx-4 flex flex-col space-y-2">
                  <CallToAction />
                  <Profile user={user} />
                </div>
              </div>
            </HamburgerMenu>
          </div>
        </div>
      </div>
    </header>
  );
}
