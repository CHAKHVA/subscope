import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-muted text-muted-foreground border-t">
      <div className="container mx-auto flex flex-col items-center justify-between gap-4 px-4 py-8 md:flex-row md:px-6">
        <p className="text-sm">
          © {new Date().getFullYear()} Subscope. All rights reserved.
        </p>
        <nav className="flex gap-4 sm:gap-6">
          <Link
            href="/terms"
            className="text-sm hover:underline underline-offset-4"
          >
            Terms of Service
          </Link>
          <Link
            href="/privacy"
            className="text-sm hover:underline underline-offset-4"
          >
            Privacy Policy
          </Link>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;
