import Link from "next/link";
import { Button } from "@/components/ui/button"; // Assuming you've added Button via shadcn/ui

const Header = () => {
  const isLoggedIn = false; // Placeholder for auth state

  return (
    <header className="bg-background border-b">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <Link href="/" className="flex items-center gap-2">
          {/* <MountainIcon className="h-6 w-6" /> You can add an SVG logo here */}
          <span className="text-lg font-semibold">Subscope</span>
        </Link>
        <nav className="hidden space-x-4 md:flex">
          {/* Placeholder nav links - will be conditional later */}
          <Link
            href="/dashboard"
            className="text-sm font-medium hover:underline underline-offset-4"
          >
            Dashboard
          </Link>
          <Link
            href="/analytics"
            className="text-sm font-medium hover:underline underline-offset-4"
          >
            Analytics
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          {isLoggedIn ? (
            <>
              {/* Placeholder for logged-in user */}
              <span className="text-sm">User Name</span>
              <Button variant="outline" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="outline" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/register">
                <Button size="sm">Sign Up</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};
export default Header;
